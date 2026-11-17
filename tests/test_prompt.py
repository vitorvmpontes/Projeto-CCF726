"""Testes do prompt do SLM e da preparação dos dados de treino."""

import json

from inference.prompt import CAMPOS, conversa_treino, mensagens, resposta
from training.preparar import amostra_estratificada


def test_resposta_compacta_com_acentos_e_so_os_5_campos():
    r = resposta([{"nome": "Sessão de Abertura", "lugar": None, "dataInicio": "2025-05-10T09:00:00-03:00",
                   "dataFim": None, "descricao": None, "secao": "x"}])
    assert "Sessão" in r and "\\u" not in r
    assert list(json.loads(r)["atividades"][0]) == list(CAMPOS)


def test_mesmo_prompt_no_treino_e_na_inferencia():
    conv = conversa_treino("TEXTO", [])
    assert conv[:1] == mensagens("TEXTO")
    assert conv[0]["content"].endswith("TEXTO") and conv[1]["role"] == "assistant"


def test_amostra_estratificada_deterministica_e_um_texto_por_evento():
    ex = [{"id": f"e{i}-{k}", "evento_id": f"e{i}", "estilo_evento": "enxuto" if i % 3 else "detalhado",
           "perfil": ["completo", "enxuto"][i % 2]} for i in range(40) for k in range(2)]
    a, b = amostra_estratificada(ex, 20, 1), amostra_estratificada(ex, 20, 1)
    assert a == b and 15 <= len(a) <= 25
    assert len({e["evento_id"] for e in a}) == len(a)
