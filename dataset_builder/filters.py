"""Limpeza da saída do professor e filtros de qualidade dos exemplos.

Cada filtro devolve uma lista de motivos de rejeição (vazia = aprovado).
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter
from functools import lru_cache
from pathlib import Path

from rapidfuzz import fuzz

from inference.postprocess import anos_do_texto, normalizar_atividade, pos_processar
from inference.schema import AtividadeExtraida

MAX_TOKENS_EXEMPLO = 7000      # entrada + saída estimadas; ajustar ao contexto do modelo
CHARS_POR_TOKEN = 3.2          # estimativa para português; a Fase 6 mede com o tokenizer real
LIMIAR_VAZAMENTO = 0.2         # fração máx. de nomes "específicos" iguais a nomes do teste
MIN_PALAVRAS_ESPECIFICO = 5    # nomes mais curtos são genéricos demais (ex.: "Sessão Técnica de Artigos")
MIN_IGUAIS_VAZAMENTO = 2       # e pelo menos 2 nomes iguais ao teste


def _sem_espaco(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").lower()
    return re.sub(r"\s+", "", s)


def _norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()


def _especifico(s: str) -> str | None:
    """Forma normalizada de nomes "específicos": sem números (ex.: "Sessão 3"
    e "Sessão 09" são genéricos) e com pelo menos 5 palavras."""
    n = re.sub(r"\s+", " ", re.sub(r"\d+[ºª°]?", " ", _norm(s))).strip()
    return n if len(n.split()) >= MIN_PALAVRAS_ESPECIFICO else None


# --------------------------------------------------------------------------
# Limpeza da saída do professor
# --------------------------------------------------------------------------

def limpar_evento(bruto: dict) -> tuple[dict | None, list[str]]:
    """Normaliza as atividades do professor (mantendo `secao`) e rejeita eventos
    com muitas atividades sem nome ou sem horário."""
    acts = bruto.get("atividades") or []
    if not acts:
        return None, ["sem_atividades"]
    correcoes: Counter = Counter()
    limpas = []
    for a in acts:
        n = normalizar_atividade(a, [], correcoes)
        if n is None or not n["dataInicio"]:
            continue
        n["secao"] = (a.get("secao") or "").strip() or None
        limpas.append(n)
    perdidas = len(acts) - len(limpas)
    if not limpas or perdidas > 0.1 * len(acts):
        return None, [f"atividades_invalidas_do_professor({perdidas}/{len(acts)})"]
    return {"evento": bruto.get("evento") or {}, "atividades": limpas}, []


# --------------------------------------------------------------------------
# Filtros de um exemplo renderizado
# --------------------------------------------------------------------------

def filtro_schema(texto: str, atividades: list[dict]) -> list[str]:
    motivos = []
    for a in atividades:
        try:
            AtividadeExtraida.model_validate(a)
        except Exception:  # noqa: BLE001
            motivos.append("schema")
            break
    pp = pos_processar(atividades, texto).atividades
    if pp != atividades:
        motivos.append("rotulo_muda_no_pos_processamento")
    return motivos


def filtro_ancoragem(texto: str, atividades: list[dict]) -> list[str]:
    """Todo nome e todo local do rótulo precisam aparecer no texto
    (ignorando espaços e quebras de linha)."""
    alvo = _sem_espaco(texto)
    motivos = []
    for a in atividades:
        if _sem_espaco(a["nome"]) not in alvo:
            motivos.append("nome_nao_ancorado")
            break
    for a in atividades:
        if a.get("lugar") and _sem_espaco(a["lugar"]) not in alvo:
            motivos.append("lugar_nao_ancorado")
            break
    return motivos


def filtro_datas(texto: str, atividades: list[dict]) -> list[str]:
    motivos = []
    anos = set(anos_do_texto(texto))
    for a in atividades:
        if not a.get("dataInicio"):
            motivos.append("sem_data_inicio")
            break
        if int(a["dataInicio"][:4]) not in anos:
            motivos.append("ano_nao_inferivel_do_texto")
            break
        if a.get("dataFim") and a["dataFim"] < a["dataInicio"]:
            motivos.append("fim_antes_do_inicio")
            break
    return motivos


def estimar_tokens(texto: str, atividades: list[dict]) -> int:
    saida = json.dumps({"atividades": atividades}, ensure_ascii=False)
    return int((len(texto) + len(saida)) / CHARS_POR_TOKEN)


def filtro_tamanho(texto: str, atividades: list[dict], max_tokens: int = MAX_TOKENS_EXEMPLO) -> list[str]:
    return ["muito_longo"] if estimar_tokens(texto, atividades) > max_tokens else []


@lru_cache(maxsize=1)
def nomes_do_teste(test_dir: str = "data/test") -> tuple[str, ...]:
    """Nomes "específicos" das atividades do conjunto de teste."""
    base = Path(test_dir)
    nomes = set()
    with (base / "manifest.csv").open(encoding="utf-8", newline="") as f:
        for r in csv.DictReader(f):
            if r.get("ground_truth"):
                for a in json.loads((base / r["ground_truth"]).read_text(encoding="utf-8")):
                    n = _especifico(a.get("nome", ""))
                    if n:
                        nomes.add(n)
    return tuple(sorted(nomes))


def filtro_vazamento(texto: str, atividades: list[dict], test_dir: str = "data/test") -> list[str]:
    """Rejeita exemplos parecidos demais com o conjunto de teste."""
    teste = nomes_do_teste(test_dir)
    especificos = [n for n in (_especifico(a["nome"]) for a in atividades) if n]
    if not especificos or not teste:
        return []
    iguais = sum(1 for n in especificos if any(fuzz.ratio(n, t) >= 90 for t in teste))
    vazou = iguais >= MIN_IGUAIS_VAZAMENTO and iguais / len(especificos) > LIMIAR_VAZAMENTO
    return ["vazamento_teste"] if vazou else []


FILTROS = [filtro_schema, filtro_ancoragem, filtro_datas, filtro_tamanho, filtro_vazamento]


def aplicar_filtros(texto: str, atividades: list[dict]) -> list[str]:
    motivos = []
    for f in FILTROS:
        motivos += f(texto, atividades)
    return motivos
