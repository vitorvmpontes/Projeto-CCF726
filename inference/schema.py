"""Contratos de dados da extração de atividades.

- `AtividadeExtraida`: o que o SLM (ou qualquer LLM) devolve. É também o
  formato dos rótulos de treino e dos gabaritos (`data/test/ground_truth`).
- `AtividadeMyMobiConf`: o objeto final enviado ao myMobiConf, montado pelo
  código a partir da `AtividadeExtraida` (campos fixos não são gerados pelo modelo).

Decisões (Fase 3, 2026-10-21):
- O modelo gera as datas já em ISO 8601 com offset -03:00.
- O modelo gera a `descricao` já em HTML (<p>, <b>, <i>, <br>).
- `dataFim` ausente no texto fica nula (não é inferida).
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field

TIMEZONE_OFFSET = "-03:00"
CONFIGURACOES_PADRAO = {"checkin": False, "perguntar": False}


class AtividadeExtraida(BaseModel):
    """Saída do modelo para uma atividade."""

    model_config = ConfigDict(extra="ignore")

    nome: str = Field(min_length=1, description="Exatamente o nome da atividade, sem descrição.")
    lugar: str | None = Field(default=None, description="Local como aparece no texto; null se ausente.")
    dataInicio: str | None = Field(default=None, description="ISO 8601 com offset -03:00; null se ausente.")
    dataFim: str | None = Field(default=None, description="ISO 8601 com offset -03:00; null se ausente.")
    descricao: str | None = Field(default=None, description="HTML (<p>, <b>, <i>, <br>) só com informação do texto.")


class SaidaExtracao(BaseModel):
    """Objeto raiz devolvido pelo modelo."""

    atividades: list[AtividadeExtraida]


class Configuracoes(BaseModel):
    checkin: bool = False
    perguntar: bool = False


class AtividadeMyMobiConf(BaseModel):
    """Objeto final aceito pelo cadastro de atividades do myMobiConf."""

    nome: str = Field(min_length=1)
    descricao: str = ""
    lugarId: str = ""  # nome do local; o frontend resolve o ID por fuzzy matching (Fuse.js)
    dataInicio: str | None = None
    dataFim: str | None = None
    tagIds: list[str] = Field(default_factory=list)
    eventoId: str = ""
    configuracoes: Configuracoes = Field(default_factory=Configuracoes)


def json_schema_saida() -> dict:
    """JSON Schema da saída do modelo, para geração restrita
    (ex.: parâmetro `format` do Ollama ou gramática do llama.cpp)."""
    return SaidaExtracao.model_json_schema()
