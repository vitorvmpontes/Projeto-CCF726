"""Testes do pós-processamento (inference/postprocess.py) e dos contratos (inference/schema.py)."""

import csv
import json
from pathlib import Path

import pytest

from evaluation.metrics import FIELDS, count, match_exact
from inference.postprocess import (
    MAX_REPETICOES_SEGUIDAS, anos_do_texto, normalizar_data, para_mymobiconf, parse_saida,
    pos_processar, sanitizar_html,
)
from inference.schema import AtividadeMyMobiConf, json_schema_saida

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "data" / "test"


# ---------------------------------------------------------------- parse

@pytest.mark.parametrize("bruto", [
    '{"atividades": [{"nome": "A"}]}',
    '[{"nome": "A"}]',
    '```json\n{"atividades": [{"nome": "A"}]}\n```',
    '<think>vou extrair</think>\n{"atividades": [{"nome": "A"}]}',
    'Aqui está o resultado: {"atividades": [{"nome": "A"}]} Espero ter ajudado.',
])
def test_parse_tolerante(bruto):
    acts, erro = parse_saida(bruto)
    assert erro == "" and acts == [{"nome": "A"}]


def test_parse_invalido():
    assert parse_saida("não é json")[0] is None
    assert pos_processar('{"outra": 1}').json_valido is False


# ---------------------------------------------------------------- datas

@pytest.mark.parametrize("entrada,esperado", [
    ("2025-09-10T09:00:00-03:00", "2025-09-10T09:00:00-03:00"),
    ("2025-09-10T09:00-03:00", "2025-09-10T09:00:00-03:00"),
    ("2025-09-10T09:00:00", "2025-09-10T09:00:00-03:00"),        # sem offset
    ("2025-09-10T09:00:00Z", "2025-09-10T09:00:00-03:00"),       # offset errado: mantém o relógio
    ("2025-9-1 9:05", "2025-09-01T09:05:00-03:00"),
    ("2S024-06-14T20:10:00-03:00", "2024-06-14T20:10:00-03:00"),  # caso real do Gemini
    ("2025-09-10", None),                                          # sem hora
    ("2025-02-30T10:00:00-03:00", None),                           # data inexistente
    ("amanhã às 9h", None),
    ("", None),
    (None, None),
])
def test_normalizar_data(entrada, esperado):
    assert normalizar_data(entrada) == esperado


def test_ano_corrigido_pelo_texto():
    assert anos_do_texto("Programação 2024 ... edição de 2023 ... 2024") == [2024, 2023]
    assert normalizar_data("2025-12-04T08:00:00-03:00", [2024]) == "2024-12-04T08:00:00-03:00"
    assert normalizar_data("2023-12-04T08:00:00-03:00", [2024, 2023]) == "2023-12-04T08:00:00-03:00"
    assert normalizar_data("2025-12-04T08:00:00-03:00", []) == "2025-12-04T08:00:00-03:00"  # texto sem ano


def test_fim_ausente_continua_nulo_e_fim_antes_do_inicio_e_anulado():
    r = pos_processar([
        {"nome": "A", "dataInicio": "2025-09-10T09:00:00-03:00"},
        {"nome": "B", "dataInicio": "2025-09-10T10:00:00-03:00", "dataFim": "2025-09-10T09:00:00-03:00"},
    ])
    assert r.atividades[0]["dataFim"] is None
    assert r.atividades[1]["dataFim"] is None
    assert r.correcoes["fim_antes_do_inicio_anulado"] == 1


# ---------------------------------------------------------------- HTML e campos

def test_sanitizar_html():
    assert sanitizar_html('<div class="x"><p style="a">Com <b>Ana</b></div>') == "<p>Com <b>Ana</b></p>"
    assert sanitizar_html("<p><b>Sem fechar") == "<p><b>Sem fechar</b></p>"
    assert sanitizar_html("<p> </p>") is None
    assert sanitizar_html("Texto puro") == "Texto puro"


def test_campos_normalizados_e_sem_nome_descartado():
    r = pos_processar([{"nome": "  Mesa   1 ", "lugarId": "  Sala A ", "descricao": ""}, {"nome": "  "}])
    assert r.atividades == [{"nome": "Mesa 1", "lugar": "Sala A", "dataInicio": None, "dataFim": None, "descricao": None}]
    assert r.correcoes["atividade_sem_nome_descartada"] == 1


def test_duplicatas_legitimas_mantidas_e_loop_cortado():
    a = {"nome": "Palestra", "lugar": "Sala", "dataInicio": "2025-09-21T19:00:00-03:00"}
    assert len(pos_processar([a, a]).atividades) == 2
    r = pos_processar([a] * 10)
    assert len(r.atividades) == MAX_REPETICOES_SEGUIDAS
    assert r.correcoes["repeticao_em_loop_removida"] == 10 - MAX_REPETICOES_SEGUIDAS


# ---------------------------------------------------------------- montagem final

def test_para_mymobiconf():
    final = para_mymobiconf(
        [{"nome": "A", "lugar": None, "dataInicio": "2025-09-10T09:00:00-03:00", "dataFim": None, "descricao": None}],
        evento_id="ev1",
    )
    assert final == [{
        "nome": "A", "descricao": "", "lugarId": "", "dataInicio": "2025-09-10T09:00:00-03:00", "dataFim": None,
        "tagIds": [], "eventoId": "ev1", "configuracoes": {"checkin": False, "perguntar": False},
    }]
    AtividadeMyMobiConf.model_validate(final[0])


def test_json_schema_da_saida():
    s = json_schema_saida()
    assert "atividades" in s["properties"]
    json.dumps(s)  # serializável para o Ollama / llama.cpp


# ---------------------------------------------------------------- gabaritos

def _rows():
    with (TEST_DIR / "manifest.csv").open(encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["avaliado"] == "sim"]


@pytest.mark.parametrize("row", _rows(), ids=lambda r: r["id"])
def test_pos_processamento_nao_altera_gabarito(row):
    """Aplicado ao gabarito, o pós-processamento não pode mudar nenhum campo avaliado."""
    gt = json.loads((TEST_DIR / row["ground_truth"]).read_text(encoding="utf-8"))
    texto = (TEST_DIR / row["raw_text"]).read_text(encoding="utf-8")
    pp = pos_processar(gt, texto).atividades
    c = count(gt, pp, match_exact(gt, pp))
    assert (c.tp, c.fp, c.fn) == (len(gt), 0, 0)
    assert all(c.field_ok[f] == c.tp for f in FIELDS)
