"""LLM professor: inventa eventos sintéticos já no formato do gabarito.

O professor devolve, para cada `EventoSpec`, um JSON com os dados do evento e
as atividades no schema congelado na Fase 3 (+ um campo auxiliar `secao`, usado
só para renderizar cabeçalhos de seção). O texto da programação NÃO é escrito
pelo LLM: ele é renderizado por código a partir deste JSON (ver render.py), o
que garante que o rótulo é correto por construção.
"""

from __future__ import annotations

import json
import time

from .spec import CASOS, EventoSpec

MODELO_PADRAO = "gemini-3.8-flash"

PROMPT = """Você é um gerador de dados para treinar um extrator de atividades de eventos brasileiros.
Invente UM evento realista, em português do Brasil, e devolva a programação completa em JSON.

Evento:
- Tipo: {tipo}
- Cidade: {cidade}
- Ano: {ano}
- Duração: {n_dias} dia(s) consecutivo(s), começando em uma data qualquer do ano {ano}
- Número de atividades: exatamente {n_atividades}
- Situações que DEVEM aparecer:
{casos}

Regras de cada atividade (são as mesmas regras do gabarito de avaliação):
- "nome": EXATAMENTE o nome da atividade, como apareceria na programação. Não coloque palestrante,
  tema, subtítulo, horário nem local no nome. Ex.: "Mesa-redonda 2", e não "Mesa-redonda 2: Avaliação e
  Responsabilidade Social – Profa. Ana".
- "lugar": nome do local (sala, auditório, bloco, espaço) ou null.
- "dataInicio" e "dataFim": ISO 8601 com offset -03:00 (ex.: "{ano}-09-10T14:00:00-03:00"). Use
  horários plausíveis. "dataFim" pode ser null quando a programação não informaria o término.
- "descricao": HTML com <p> para parágrafos, <b> em TODOS os nomes de pessoas (palestrantes,
  autores, coordenadores) e <i> em títulos de palestras/trabalhos; ou null quando a atividade não
  tem informação adicional (ex.: coffee break). Tema/subtítulo da atividade vai aqui.
- "secao": cabeçalho de grupo ao qual a atividade pertence na programação (ex.: "Sessões Técnicas",
  "Minicursos", "Programação Cultural") ou null. Use seções em parte dos eventos.

Diversidade (importante — o dataset terá centenas de eventos):
- Varie nomes de pessoas, instituições, temas, horários e salas.
- Não comece sempre com credenciamento nem use sempre "Conferência Magna", "Mesa-redonda" ou
  "Coffee Break": use os nomes típicos DESTE tipo de evento.
- Títulos longos são para palestras, oficinas, trabalhos e mesas. Intervalos, almoço,
  credenciamento e encerramento têm nomes curtos.
- "secao" agrupa VÁRIAS atividades do mesmo tipo (ex.: 3 minicursos em "Minicursos"); não crie
  uma seção para cada atividade. Atividades isoladas ficam com "secao": null.
Ordene as atividades por data e horário.
"""

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "evento": {
            "type": "object",
            "properties": {"nome": {"type": "string"}, "local_geral": {"type": ["string", "null"]}},
            "required": ["nome"],
        },
        "atividades": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "nome": {"type": "string"},
                    "lugar": {"type": ["string", "null"]},
                    "dataInicio": {"type": "string"},
                    "dataFim": {"type": ["string", "null"]},
                    "descricao": {"type": ["string", "null"]},
                    "secao": {"type": ["string", "null"]},
                },
                "required": ["nome", "dataInicio"],
            },
        },
    },
    "required": ["evento", "atividades"],
}


def montar_prompt(spec: EventoSpec) -> str:
    casos = "\n".join(f"  - {CASOS[c]}" for c in spec.casos)
    return PROMPT.format(
        tipo=spec.tipo, cidade=spec.cidade, ano=spec.ano, n_dias=spec.n_dias,
        n_atividades=spec.n_atividades, casos=casos,
    )


def gerar_evento(client, spec: EventoSpec, modelo: str = MODELO_PADRAO, tentativas: int = 5) -> tuple[dict, dict]:
    """Chama o professor e devolve (evento, uso_de_tokens)."""
    from google.genai import errors, types

    config = types.GenerateContentConfig(
        temperature=1.0,
        response_mime_type="application/json",
        response_json_schema=RESPONSE_SCHEMA,
        thinking_config=types.ThinkingConfig(thinking_level="LOW"),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    espera = 5.0
    for t in range(1, tentativas + 1):
        try:
            resp = client.models.generate_content(model=modelo, contents=montar_prompt(spec), config=config)
            dados = json.loads(resp.text)
            u = resp.usage_metadata
            uso = {
                "entrada": u.prompt_token_count or 0,
                "saida": (u.candidates_token_count or 0) + (u.thoughts_token_count or 0),
            }
            return dados, uso
        except (errors.APIError, json.JSONDecodeError) as e:
            code = getattr(e, "code", None)
            if t < tentativas and (code in (429, 500, 502, 503, 504) or isinstance(e, json.JSONDecodeError)):
                time.sleep(espera)
                espera *= 2
                continue
            raise
    raise RuntimeError("inalcançável")
