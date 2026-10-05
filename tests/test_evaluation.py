"""Testes do script de avaliação (evaluation/)."""

import csv
import importlib.util
import json
from pathlib import Path

import pytest

from evaluation.evaluate import bootstrap_ci, run
from evaluation.loading import load_activities
from evaluation.metrics import (
    Counts, count, field_correct, match_exact, match_fuzzy, normalize_activity, strip_html,
)

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "data" / "test"
MANIFEST = TEST_DIR / "manifest.csv"


def _rows():
    with MANIFEST.open(encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["avaliado"] == "sim"]


def _legacy():
    spec = importlib.util.spec_from_file_location("script1", ROOT / "evaluation" / "legacy_tcc" / "script1.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- regressão

@pytest.mark.parametrize("row", _rows(), ids=lambda r: r["id"])
def test_nivel1_exato_igual_ao_script_do_tcc(row):
    """O Nível 1 (exato) deve dar exatamente o mesmo TP/FP/FN que o script1.py do TCC."""
    legacy = _legacy()
    gt = json.loads((TEST_DIR / row["ground_truth"]).read_text(encoding="utf-8"))
    pred = json.loads((TEST_DIR / row["baseline_gemini"]).read_text(encoding="utf-8"))
    tp, fp, fn, _ = legacy.compare_activities(gt, pred)
    c = count(gt, pred, match_exact(gt, pred))
    assert (c.tp, c.fp, c.fn) == (tp, fp, fn)


@pytest.mark.parametrize("row", _rows(), ids=lambda r: r["id"])
def test_gabaritos_validos_no_schema(row):
    loaded = load_activities(TEST_DIR / row["ground_truth"])
    assert loaded.json_valid
    assert loaded.schema_errors == []


def test_run_baseline_completo():
    res = run(MANIFEST, TEST_DIR / "baseline_gemini", 0.9, n_boot=200, seed=1)
    assert res["arquivos_avaliados"] == 17
    ex, ap = res["exato"], res["aproximado"]
    assert ap["tp"] >= ex["tp"]  # o casamento aproximado nunca acha menos pares
    lo, hi = ex["ic95_bootstrap"]["f1"]
    assert lo <= ex["f1"] <= hi


# ---------------------------------------------------------------- unidade

def test_lugarid_e_sinonimo_de_lugar():
    assert normalize_activity({"lugarId": "Sala 1"})["lugar"] == "Sala 1"
    assert normalize_activity({"lugar": "A", "lugarId": "B"})["lugar"] == "A"


def test_nulo_e_vazio_sao_equivalentes():
    for f in ("lugar", "descricao", "dataInicio", "dataFim"):
        assert field_correct(f, {f: None}, {f: ""})
        assert field_correct(f, {}, {f: None})


def test_descricao_ignora_tags_html():
    gt = {"descricao": "<p><b>Coordenador:</b> Ana</p><p>Sala &amp; auditório</p>"}
    pred = {"descricao": "Coordenador: <i>Ana</i>\nSala & auditório"}
    assert field_correct("descricao", gt, pred)
    assert strip_html("<p>a</p><p>b</p>") == "a b"


def test_descricao_por_similaridade_e_inventada_conta_erro():
    gt = {"descricao": "<p>Atividade organizada pela Comissão de Cultura e Extensão</p>"}
    assert field_correct("descricao", gt, {"descricao": "Atividade organizada pela Comissão de Cultura e Extensão."})
    assert not field_correct("descricao", gt, {"descricao": "Mesa redonda sobre avaliação institucional"})
    assert not field_correct("descricao", {"descricao": None}, {"descricao": "<p>Palestra sobre o tema.</p>"})
    assert not field_correct("descricao", gt, {"descricao": ""})


def test_datas_comparadas_como_datetime():
    assert field_correct("dataInicio", {"dataInicio": "2025-09-10T09:00:00-03:00"},
                         {"dataInicio": "2025-09-10T09:00-03:00"})
    assert not field_correct("dataInicio", {"dataInicio": "2025-09-10T09:00:00-03:00"},
                             {"dataInicio": "2025-09-10T09:00:00"})


def test_match_exato_um_para_um_com_nomes_repetidos():
    gt = [{"nome": "Coffee Break"}, {"nome": "Coffee Break"}, {"nome": "Abertura"}]
    pred = [{"nome": " coffee break "}, {"nome": "Coffee Break"}, {"nome": "Coffee Break"}, {"nome": ""}]
    assert len(match_exact(gt, pred)) == 2


def test_match_aproximado_respeita_limiar():
    gt = [{"nome": "Palestra: Desmistificando a Inteligência Artificial"}]
    pred = [{"nome": "PALESTRA - DESMISTIFICANDO A INTELIGENCIA ARTIFICIAL"}]
    assert len(match_exact(gt, pred)) == 0
    assert len(match_fuzzy(gt, pred, 0.9)) == 1
    assert len(match_fuzzy([{"nome": "Abertura"}], [{"nome": "Encerramento"}], 0.9)) == 0
    # nome só com pontuação (existe no opmed-html) também deve casar
    assert len(match_fuzzy([{"nome": "-"}], [{"nome": " - "}], 0.9)) == 1


def test_predicao_ausente_ou_invalida(tmp_path):
    assert not load_activities(tmp_path / "nao_existe.json").json_valid
    bad = tmp_path / "x.json"
    bad.write_text("isto não é json", encoding="utf-8")
    assert not load_activities(bad).json_valid
    ok = tmp_path / "y.json"
    ok.write_text(json.dumps({"atividades": [{"nome": "A", "dataInicio": "ontem"}]}), encoding="utf-8")
    loaded = load_activities(ok)
    assert loaded.json_valid and loaded.n_total == 1 and loaded.schema_valid == 0


def test_bootstrap_deterministico():
    files = [Counts(5, 1, 0), Counts(3, 0, 2), Counts(10, 2, 1)]
    assert bootstrap_ci(files, 500, seed=7) == bootstrap_ci(files, 500, seed=7)
