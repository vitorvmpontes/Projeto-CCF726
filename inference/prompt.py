"""Prompt do SLM: o MESMO texto no treino, na validação e na inferência.

O prompt é curto de propósito: o formato e as regras de anotação são
aprendidos no fine-tuning, não explicados no prompt (o prompt longo do TCC
custaria ~1.000 tokens por chamada). Só há uma mensagem de usuário, sem
mensagem de sistema, para não depender de como cada template trata o papel
"system".

Este módulo só usa a biblioteca padrão, para rodar igual no Colab e no PC.
"""

from __future__ import annotations

import json

VERSAO_PROMPT = "v1"

INSTRUCAO = (
    "Extraia as atividades da programação de evento abaixo. Responda apenas com JSON no formato "
    '{"atividades": [{"nome": ..., "lugar": ..., "dataInicio": ..., "dataFim": ..., "descricao": ...}]}. '
    "Datas em ISO 8601 com -03:00; campo ausente no texto = null; descricao em HTML."
)

CAMPOS = ("nome", "lugar", "dataInicio", "dataFim", "descricao")


def mensagem_usuario(texto: str) -> str:
    return f"{INSTRUCAO}\n\nProgramação:\n{texto.strip()}"


def mensagens(texto: str) -> list[dict]:
    """Conversa de inferência (só o turno do usuário)."""
    return [{"role": "user", "content": mensagem_usuario(texto)}]


def resposta(atividades: list[dict]) -> str:
    """Resposta-alvo do treino: JSON compacto, acentos literais, só os 5 campos."""
    limpas = [{c: a.get(c) for c in CAMPOS} for a in atividades]
    return json.dumps({"atividades": limpas}, ensure_ascii=False)


def conversa_treino(texto: str, atividades: list[dict]) -> list[dict]:
    """Conversa completa de treino (usuário + modelo)."""
    return mensagens(texto) + [{"role": "assistant", "content": resposta(atividades)}]
