"""Testes do construtor de dataset (dataset_builder/), sem chamar a API."""

import json
import random
from pathlib import Path

import pytest

from dataset_builder.filters import aplicar_filtros, filtro_ancoragem, filtro_vazamento, limpar_evento
from dataset_builder.render import LAYOUTS, RUIDOS, renderizar
from dataset_builder.spec import sortear_specs
from dataset_builder.teacher import RESPONSE_SCHEMA, montar_prompt

ROOT = Path(__file__).resolve().parents[1]

EVENTO = {
    "evento": {"nome": "Semana de Computação"},
    "atividades": [
        {"nome": "Credenciamento", "lugar": "Hall do Bloco A", "dataInicio": "2025-10-20T08:00:00-03:00",
         "dataFim": "2025-10-20T09:00:00-03:00", "descricao": None, "secao": None},
        {"nome": "Minicurso de Aprendizado de Máquina com scikit-learn para iniciantes", "lugar": "Lab 3",
         "dataInicio": "2025-10-20T09:00:00-03:00", "dataFim": "2025-10-20T12:00:00-03:00",
         "descricao": "<p><b>Ministrante:</b> <b>Ana Souza</b></p><p>Traga seu notebook.</p>", "secao": "Minicursos"},
        {"nome": "Minicurso de Git", "lugar": "Lab 4", "dataInicio": "2025-10-20T09:00:00-03:00",
         "dataFim": "2025-10-20T12:00:00-03:00", "descricao": None, "secao": "Minicursos"},
        {"nome": "Coffee break", "lugar": None, "dataInicio": "2025-10-21T10:00:00-03:00",
         "dataFim": None, "descricao": None, "secao": None},
        {"nome": "Palestra de encerramento", "lugar": "Auditório", "dataInicio": "2025-10-21T16:00:00-03:00",
         "dataFim": "2025-10-21T17:00:00-03:00", "descricao": "<p>Tema: <i>Futuro da IA</i></p>", "secao": None},
    ],
}


def test_specs_deterministicas():
    a, b = sortear_specs(10, 3), sortear_specs(10, 3)
    assert [s.to_dict() for s in a] == [s.to_dict() for s in b]
    assert all(s.n_atividades >= 3 for s in a)


def test_prompt_do_professor_contem_regras_e_spec():
    s = sortear_specs(1, 1)[0]
    p = montar_prompt(s)
    assert str(s.ano) in p and "EXATAMENTE o nome da atividade" in p
    assert set(RESPONSE_SCHEMA["required"]) == {"evento", "atividades"}


@pytest.mark.parametrize("layout", LAYOUTS)
@pytest.mark.parametrize("semente", range(6))
def test_render_passa_nos_filtros(layout, semente):
    rng = random.Random(semente)
    ruidos = [r for r in RUIDOS if rng.random() < 0.5]
    r = renderizar(EVENTO, layout, rng, ruidos)
    assert aplicar_filtros(r.texto, r.atividades) == []
    assert len(r.atividades) == len(EVENTO["atividades"])
    assert "2025" in r.texto  # o ano sempre aparece
    assert all("secao" not in a for a in r.atividades)


def test_cartaz_em_caixa_alta_e_rotulo_acompanha():
    r = renderizar(EVENTO, "cartaz", random.Random(0), [])
    assert r.atividades[0]["nome"] == "CREDENCIAMENTO"
    assert r.atividades[0]["lugar"] == "HALL DO BLOCO A"
    assert "CREDENCIAMENTO" in r.texto


def test_secoes_aparecem_mas_nao_viram_atividade():
    r = renderizar(EVENTO, "lista", random.Random(1), ["secoes"])
    assert "minicursos" in r.texto.lower()
    assert all(a["nome"].lower() != "minicursos" for a in r.atividades)


def test_secao_de_uma_atividade_so_nao_vira_cabecalho():
    ev = {"evento": {"nome": "X"}, "atividades": [dict(EVENTO["atividades"][3], secao="Encerramento")]}
    r = renderizar(ev, "lista", random.Random(1), ["secoes"])
    assert "Encerramento\n" not in r.texto and "ENCERRAMENTO\n" not in r.texto


def test_descricao_renderizada_no_texto():
    r = renderizar(EVENTO, "colunas", random.Random(2), [])
    assert "Ministrante: Ana Souza" in r.texto and "Traga seu notebook." in r.texto


def test_ancoragem_reprova_nome_ausente():
    r = renderizar(EVENTO, "lista", random.Random(3), [])
    atividades = [dict(a) for a in r.atividades]
    atividades[0]["nome"] = "Atividade que não está no texto"
    assert "nome_nao_ancorado" in filtro_ancoragem(r.texto, atividades)


def test_limpar_evento():
    ev, motivos = limpar_evento(EVENTO)
    assert motivos == [] and ev["atividades"][1]["secao"] == "Minicursos"
    ruim = {"atividades": [{"nome": "", "dataInicio": "x"}] * 3 + EVENTO["atividades"][:4]}
    assert limpar_evento(ruim)[0] is None


def test_vazamento_detecta_evento_do_teste():
    gt = json.loads((ROOT / "data/test/ground_truth/semanaacademicausp-pdf.json").read_text(encoding="utf-8"))
    assert filtro_vazamento("", gt, str(ROOT / "data/test")) == ["vazamento_teste"]
    genericos = [{"nome": f"Sessão Técnica de Artigos {i}"} for i in range(10)]
    assert filtro_vazamento("", genericos, str(ROOT / "data/test")) == []
