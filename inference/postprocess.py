"""Pós-processamento determinístico da saída do modelo.

O modelo já entrega datas em ISO 8601 e a descrição em HTML. Este módulo não
inventa informação: ele valida, corrige problemas de formato e monta o objeto
final do myMobiConf.

Etapas (`pos_processar`):
1. `parse_saida`: extrai o JSON da resposta bruta (tolera cercas ```json,
   blocos <think> e texto antes/depois do JSON).
2. Para cada atividade:
   - `nome`: espaços normalizados; atividade sem nome é descartada.
   - `lugar`: espaços normalizados; vazio vira null.
   - datas: `normalizar_data` aceita variações de ISO 8601, força o offset
     -03:00 (todos os horários do texto são de America/Sao_Paulo), repara
     anos com caractere espúrio ("2S024" -> "2024") e devolve null para
     valores que não são datas. O ano é corrigido pelo texto
     (`anos_do_texto`): se o texto cita anos e o ano da data não está entre
     eles, usa-se o ano mais citado.
   - `dataFim` ausente continua nula; `dataFim` anterior a `dataInicio` vira nula.
   - `descricao`: HTML sanitizado (só <p>, <b>, <i>, <br>, <hr>, sem atributos,
     tags balanceadas); vazia vira null.
3. Corta repetições idênticas seguidas além de MAX_REPETICOES_SEGUIDAS
   (sinal de modelo em loop). Duplicatas legítimas são mantidas.

`para_mymobiconf` monta o objeto final, injetando os campos fixos
(`eventoId`, `tagIds`, `configuracoes`), que não são gerados pelo modelo.
Todas as correções ficam registradas em `Resultado.correcoes`.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from .schema import CONFIGURACOES_PADRAO, TIMEZONE_OFFSET, AtividadeExtraida, AtividadeMyMobiConf

TAGS_PERMITIDAS = {"p", "b", "i", "br", "hr"}
# Programações reais podem repetir uma atividade idêntica (ex.: SEBRAE lista a
# mesma palestra duas vezes). Só cortamos repetições seguidas além disso, que
# indicam o modelo preso em loop.
MAX_REPETICOES_SEGUIDAS = 2

_ISO_RE = re.compile(
    r"^\s*(\d{4})-(\d{1,2})-(\d{1,2})"          # data
    r"(?:[T ](\d{1,2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?)?"  # hora opcional
    r"\s*(Z|[+-]\d{2}:?\d{2})?\s*$"              # offset opcional
)
_ANO_RE = re.compile(r"(?<!\d)(20\d{2})(?!\d)")


@dataclass
class Resultado:
    atividades: list[dict] = field(default_factory=list)
    json_valido: bool = True
    erro: str = ""
    correcoes: Counter = field(default_factory=Counter)


# --------------------------------------------------------------------------
# 1. Parse da resposta bruta
# --------------------------------------------------------------------------

def parse_saida(bruto: str | dict | list) -> tuple[list[dict] | None, str]:
    """Devolve (lista de atividades, mensagem de erro)."""
    if isinstance(bruto, list):
        return [a for a in bruto if isinstance(a, dict)], ""
    if isinstance(bruto, dict):
        acts = bruto.get("atividades")
        return ([a for a in acts if isinstance(a, dict)], "") if isinstance(acts, list) else (None, "sem 'atividades'")

    texto = re.sub(r"<think>.*?</think>", "", bruto or "", flags=re.DOTALL)
    texto = re.sub(r"```(?:json)?", "", texto).strip()
    candidatos = [texto]
    for abre, fecha in (("{", "}"), ("[", "]")):
        i, j = texto.find(abre), texto.rfind(fecha)
        if i != -1 and j > i:
            candidatos.append(texto[i : j + 1])
    for c in candidatos:
        try:
            dados = json.loads(c)
        except json.JSONDecodeError:
            continue
        acts, erro = parse_saida(dados)
        if acts is not None:
            return acts, ""
    return None, "JSON inválido"


# --------------------------------------------------------------------------
# 2. Normalização de campos
# --------------------------------------------------------------------------

def _texto_limpo(v: Any) -> str | None:
    if v is None:
        return None
    s = re.sub(r"\s+", " ", str(v)).strip()
    return s or None


def anos_do_texto(texto: str | None) -> list[int]:
    """Anos (20xx) citados no texto de entrada, do mais para o menos frequente."""
    if not texto:
        return []
    return [int(a) for a, _ in Counter(_ANO_RE.findall(texto)).most_common()]


def normalizar_data(valor: Any, anos: list[int] | None = None, correcoes: Counter | None = None) -> str | None:
    """Converte para 'AAAA-MM-DDTHH:MM:SS-03:00' ou devolve None.

    - Data sem hora vira None (não é um horário de atividade).
    - Offset ausente ou diferente de -03:00: mantém a hora do relógio e
      aplica -03:00 (os horários do texto são sempre de São Paulo).
    - Ano fora dos anos citados no texto: troca pelo ano mais citado.
    """
    c = correcoes if correcoes is not None else Counter()
    if valor is None or (isinstance(valor, str) and not valor.strip()):
        return None
    texto = str(valor).strip()
    # Repara ano com caractere espúrio (ex.: "2S024-..." gerado pelo Gemini)
    tok = re.match(r"^([0-9A-Za-z]{5,6})-", texto)
    if tok and len(re.sub(r"\D", "", tok.group(1))) == 4:
        texto = re.sub(r"\D", "", tok.group(1)) + texto[len(tok.group(1)):]
        c["ano_malformado_reparado"] += 1
    m = _ISO_RE.match(texto)
    if not m:
        c["data_invalida_descartada"] += 1
        return None
    ano, mes, dia, hh, mm, ss, tz = m.groups()
    if hh is None:
        c["data_sem_hora_descartada"] += 1
        return None
    ano = int(ano)
    if anos and ano not in anos:
        c["ano_corrigido_pelo_texto"] += 1
        ano = anos[0]
    try:
        dt = datetime(ano, int(mes), int(dia), int(hh), int(mm), int(ss or 0))
    except ValueError:
        c["data_invalida_descartada"] += 1
        return None
    if tz is None:
        c["offset_adicionado"] += 1
    elif tz.replace(":", "") != TIMEZONE_OFFSET.replace(":", ""):
        c["offset_ajustado"] += 1
    return dt.strftime("%Y-%m-%dT%H:%M:%S") + TIMEZONE_OFFSET


def sanitizar_html(valor: Any, correcoes: Counter | None = None) -> str | None:
    """Mantém só as tags permitidas, sem atributos, e devolve HTML bem formado."""
    from bs4 import BeautifulSoup

    c = correcoes if correcoes is not None else Counter()
    if valor is None:
        return None
    original = str(valor).strip()
    if not original:
        return None
    soup = BeautifulSoup(original, "html.parser")  # fecha tags abertas
    for tag in soup.find_all(True):
        if tag.name not in TAGS_PERMITIDAS:
            tag.unwrap()
            c["tag_html_removida"] += 1
        elif tag.attrs:
            tag.attrs = {}
            c["atributo_html_removido"] += 1
    if not soup.get_text(strip=True):
        return None
    return str(soup).strip()


def normalizar_atividade(bruta: dict, anos: list[int], correcoes: Counter) -> dict | None:
    nome = _texto_limpo(bruta.get("nome"))
    if not nome:
        correcoes["atividade_sem_nome_descartada"] += 1
        return None
    lugar = _texto_limpo(bruta.get("lugar", bruta.get("lugarId")))
    ini = normalizar_data(bruta.get("dataInicio"), anos, correcoes)
    fim = normalizar_data(bruta.get("dataFim"), anos, correcoes)
    if ini and fim and fim < ini:
        correcoes["fim_antes_do_inicio_anulado"] += 1
        fim = None
    desc = sanitizar_html(bruta.get("descricao"), correcoes)
    ativ = AtividadeExtraida(nome=nome, lugar=lugar, dataInicio=ini, dataFim=fim, descricao=desc)
    return ativ.model_dump()


# --------------------------------------------------------------------------
# 3. Pipeline e montagem final
# --------------------------------------------------------------------------

def pos_processar(bruto: str | dict | list, texto_entrada: str | None = None) -> Resultado:
    """Aplica todas as etapas à resposta do modelo.

    `texto_entrada` é o texto bruto da programação; serve para corrigir o ano.
    """
    acts, erro = parse_saida(bruto)
    if acts is None:
        return Resultado(json_valido=False, erro=erro)
    res = Resultado()
    anos = anos_do_texto(texto_entrada)
    anterior, seguidas = None, 0
    for a in acts:
        n = normalizar_atividade(a, anos, res.correcoes)
        if n is None:
            continue
        chave = (n["nome"].lower(), n["lugar"], n["dataInicio"], n["dataFim"])
        seguidas = seguidas + 1 if chave == anterior else 1
        anterior = chave
        if seguidas > MAX_REPETICOES_SEGUIDAS:
            res.correcoes["repeticao_em_loop_removida"] += 1
            continue
        res.atividades.append(n)
    return res


def para_mymobiconf(
    atividades: list[dict],
    evento_id: str = "",
    tag_ids: list[str] | None = None,
    configuracoes: dict | None = None,
) -> list[dict]:
    """Monta e valida os objetos finais do myMobiConf."""
    cfg = configuracoes or CONFIGURACOES_PADRAO
    saida = []
    for a in atividades:
        obj = AtividadeMyMobiConf(
            nome=a["nome"],
            descricao=a.get("descricao") or "",
            lugarId=a.get("lugar") or "",
            dataInicio=a.get("dataInicio"),
            dataFim=a.get("dataFim"),
            tagIds=list(tag_ids or []),
            eventoId=evento_id,
            configuracoes=cfg,
        )
        saida.append(obj.model_dump())
    return saida
