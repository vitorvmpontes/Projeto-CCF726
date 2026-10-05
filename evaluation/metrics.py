"""Métricas de avaliação da extração de atividades.

Níveis (ver docs/PLANEJAMENTO.md, seção 8):
- Nível 1  — detecção, casamento por `nome` exato (critério do TCC:
             `lower().strip()`, emparelhamento guloso um-para-um).
- Nível 1b — detecção, casamento aproximado por similaridade de string.
- Nível 2  — acurácia por campo nas atividades emparelhadas.

Regras de comparação dos campos (Nível 2):
- `lugar`: texto normalizado (minúsculas, espaços colapsados). `lugarId` é
  tratado como sinônimo de `lugar`.
- `dataInicio` / `dataFim`: comparadas como datetime (ISO 8601); se não for
  possível interpretar, compara-se o texto normalizado.
- `descricao`: as tags HTML NÃO são avaliadas. Remove-se o HTML, decodificam-se
  entidades e compara-se o texto normalizado por similaridade
  (`rapidfuzz.fuzz.ratio` >= DESC_THRESHOLD). Descrição inventada quando o
  gabarito não tem descrição (ou o contrário) conta como erro.
- Ausente, `null` e `""` são equivalentes em todos os campos.
"""

from __future__ import annotations

import html
import re
import unicodedata
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from rapidfuzz import fuzz

FIELDS = ("lugar", "dataInicio", "dataFim", "descricao")
DESC_THRESHOLD = 0.9  # similaridade mínima para a descrição contar como correta


# --------------------------------------------------------------------------
# Normalização
# --------------------------------------------------------------------------

def norm_name_exact(value: Any) -> str:
    """Normalização do TCC (script1.py): minúsculas e strip."""
    return value.lower().strip() if isinstance(value, str) else ""


def norm_name_fuzzy(value: Any) -> str:
    """Normalização para o casamento aproximado: sem acento, sem pontuação."""
    if not isinstance(value, str):
        return ""
    s = unicodedata.normalize("NFKD", value)
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_text(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value)).strip().lower()


def strip_html(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    s = re.sub(r"<[^>]+>", " ", value)
    return norm_text(html.unescape(s))


def parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        return datetime.fromisoformat(value.strip())
    except ValueError:
        return None


def same_datetime(a: Any, b: Any) -> bool:
    da, db = parse_datetime(a), parse_datetime(b)
    if da is not None and db is not None:
        if (da.tzinfo is None) != (db.tzinfo is None):
            return False
        return da == db
    return norm_text(a) == norm_text(b)


def normalize_activity(act: dict) -> dict:
    """Unifica nomes de campo (`lugarId` -> `lugar`)."""
    out = dict(act)
    if "lugar" not in out and "lugarId" in out:
        out["lugar"] = out["lugarId"]
    return out


def field_correct(field_name: str, gt: dict, pred: dict) -> bool:
    g, p = gt.get(field_name), pred.get(field_name)
    if field_name in ("dataInicio", "dataFim"):
        return same_datetime(g, p)
    if field_name == "descricao":
        gd, pd = strip_html(g), strip_html(p)
        if not gd or not pd:
            return gd == pd  # vazia × vazia = acerto; inventada ou omitida = erro
        return gd == pd or fuzz.ratio(gd, pd) / 100.0 >= DESC_THRESHOLD
    return norm_text(g) == norm_text(p)


# --------------------------------------------------------------------------
# Emparelhamento
# --------------------------------------------------------------------------

def match_exact(gt: list[dict], pred: list[dict]) -> list[tuple[int, int]]:
    """Emparelhamento do TCC: percorre as predições em ordem e associa cada uma
    à primeira atividade do gabarito, ainda livre, com o mesmo nome normalizado."""
    free_gt = list(range(len(gt)))
    pairs = []
    for j, p in enumerate(pred):
        pn = norm_name_exact(p.get("nome"))
        if not pn:
            continue
        for k, i in enumerate(free_gt):
            if norm_name_exact(gt[i].get("nome")) == pn:
                pairs.append((i, j))
                del free_gt[k]
                break
    return pairs


def match_fuzzy(gt: list[dict], pred: list[dict], threshold: float = 0.9) -> list[tuple[int, int, float]]:
    """Emparelhamento guloso pela maior similaridade (rapidfuzz ratio, 0-1),
    aceitando apenas pares com similaridade >= threshold."""
    # Nomes só com pontuação (ex.: "-") ficariam vazios: usa a forma exata.
    def key(a):
        return norm_name_fuzzy(a.get("nome")) or norm_name_exact(a.get("nome"))

    gn = [key(a) for a in gt]
    pn = [key(a) for a in pred]
    cands = []
    for i, g in enumerate(gn):
        if not g:
            continue
        for j, p in enumerate(pn):
            if not p:
                continue
            s = 1.0 if g == p else fuzz.ratio(g, p) / 100.0
            if s >= threshold:
                cands.append((-s, i, j))
    cands.sort()
    used_g, used_p, pairs = set(), set(), []
    for neg_s, i, j in cands:
        if i in used_g or j in used_p:
            continue
        used_g.add(i)
        used_p.add(j)
        pairs.append((i, j, -neg_s))
    return pairs


# --------------------------------------------------------------------------
# Contagens e métricas
# --------------------------------------------------------------------------

@dataclass
class Counts:
    tp: int = 0
    fp: int = 0
    fn: int = 0
    field_ok: dict[str, int] = field(default_factory=lambda: {f: 0 for f in FIELDS})

    def __add__(self, other: "Counts") -> "Counts":
        return Counts(
            self.tp + other.tp,
            self.fp + other.fp,
            self.fn + other.fn,
            {f: self.field_ok[f] + other.field_ok[f] for f in FIELDS},
        )

    @property
    def precision(self) -> float:
        return self.tp / (self.tp + self.fp) if self.tp + self.fp else 0.0

    @property
    def recall(self) -> float:
        return self.tp / (self.tp + self.fn) if self.tp + self.fn else 0.0

    @property
    def f1(self) -> float:
        p, r = self.precision, self.recall
        return 2 * p * r / (p + r) if p + r else 0.0

    def field_accuracy(self) -> dict[str, float]:
        return {f: (self.field_ok[f] / self.tp if self.tp else 0.0) for f in FIELDS}


def count(gt: list[dict], pred: list[dict], pairs: list[tuple]) -> Counts:
    gt = [normalize_activity(a) for a in gt]
    pred = [normalize_activity(a) for a in pred]
    c = Counts(tp=len(pairs), fp=len(pred) - len(pairs), fn=len(gt) - len(pairs))
    for pair in pairs:
        i, j = pair[0], pair[1]
        for f in FIELDS:
            if field_correct(f, gt[i], pred[j]):
                c.field_ok[f] += 1
    return c


def evaluate_pair(gt: list[dict], pred: list[dict], fuzzy_threshold: float = 0.9) -> dict[str, Counts]:
    return {
        "exato": count(gt, pred, match_exact(gt, pred)),
        "aproximado": count(gt, pred, match_fuzzy(gt, pred, fuzzy_threshold)),
    }
