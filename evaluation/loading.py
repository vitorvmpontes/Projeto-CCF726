"""Leitura das predições/gabaritos e validação de formato (JSON e schema)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ATIVIDADE_SCHEMA = {
    "type": "object",
    "required": ["nome"],
    "properties": {
        "nome": {"type": "string", "minLength": 1},
        "lugar": {"type": ["string", "null"]},
        "lugarId": {"type": ["string", "null"]},
        "descricao": {"type": ["string", "null"]},
        "dataInicio": {"$ref": "#/$defs/data"},
        "dataFim": {"$ref": "#/$defs/data"},
    },
    "$defs": {
        "data": {
            "anyOf": [
                {"type": "null"},
                {"type": "string", "maxLength": 0},
                {
                    "type": "string",
                    # ISO 8601 com offset obrigatório, ex.: 2025-09-10T09:00:00-03:00
                    "pattern": r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2})?([+-]\d{2}:\d{2}|Z)$",
                },
            ]
        }
    },
}

_validator = Draft202012Validator(ATIVIDADE_SCHEMA, format_checker=FormatChecker())


@dataclass
class Loaded:
    activities: list[dict] = field(default_factory=list)
    exists: bool = True
    json_valid: bool = True
    error: str = ""
    n_total: int = 0  # itens na lista de atividades
    schema_valid: int = 0  # atividades válidas no schema
    schema_errors: list[str] = field(default_factory=list)


def load_activities(path: str | Path) -> Loaded:
    """Lê um JSON de atividades: aceita uma lista ou {"atividades": [...]}.

    Arquivo ausente ou JSON inválido não interrompe a avaliação: devolve lista
    vazia e marca o problema (todas as atividades do gabarito viram FN).
    """
    path = Path(path)
    if not path.exists():
        return Loaded(exists=False, json_valid=False, error="arquivo ausente")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        return Loaded(json_valid=False, error=f"JSON inválido: {e}")

    if isinstance(data, dict) and isinstance(data.get("atividades"), list):
        acts = data["atividades"]
    elif isinstance(data, list):
        acts = data
    else:
        return Loaded(json_valid=False, error="raiz não é lista nem {'atividades': [...]}")

    loaded = Loaded(activities=[a for a in acts if isinstance(a, dict)], n_total=len(acts))
    for k, a in enumerate(acts):
        errs = sorted(_validator.iter_errors(a), key=lambda e: list(e.path)) if isinstance(a, dict) else ["não é objeto"]
        if errs:
            first = errs[0]
            msg = first if isinstance(first, str) else f"{'/'.join(map(str, first.path)) or '<raiz>'}: {first.message}"
            loaded.schema_errors.append(f"atividade {k}: {msg}")
        else:
            loaded.schema_valid += 1
    return loaded
