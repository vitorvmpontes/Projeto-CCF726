"""Renderiza um evento (JSON) como o texto bruto de uma programação.

O texto imita o que sai da fase 1 do pipeline (PyMuPDF, OCR, HTML, planilha),
com layouts e ruídos variados. Toda informação do rótulo aparece no texto,
então a regra "descrição determinística / só informação do texto" vale por
construção. Quando um ruído muda a forma do nome no texto (ex.: CAIXA ALTA),
o rótulo acompanha, porque o `nome` é "exatamente como aparece".

Layouts:
- lista:    um bloco por atividade (horário, nome, local, descrição), dias como cabeçalhos
- tabela:   uma linha por atividade, colunas separadas por " | " (como a planilha) ou tab
- colunas:  cada campo numa linha, com cabeçalho "Horário / Atividade / Local" (como PDF/HTML)
- cartaz:   estilo arte de divulgação passada por OCR: CAIXA ALTA, horário em linha separada,
            textos decorativos

Ruídos (independentes do layout):
- secoes:      cabeçalhos de seção que NÃO são atividades
- decorativo:  linhas soltas de patrocínio, redes sociais, avisos
- quebra:      títulos longos quebrados em várias linhas
- ocr:         erros de OCR em linhas que não são nome (decorativo, descrição)
"""

from __future__ import annotations

import html
import random
import re
import textwrap
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime

LAYOUTS = ["lista", "tabela", "colunas", "cartaz"]
RUIDOS = ["secoes", "decorativo", "quebra", "ocr"]

DIAS_SEMANA = ["Segunda-feira", "Terça-feira", "Quarta-feira", "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"]
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto",
         "setembro", "outubro", "novembro", "dezembro"]
DECORATIVOS = [
    "Siga @{sigla} nas redes sociais", "Realização:", "Apoio:", "Patrocínio", "Inscrições gratuitas",
    "Vagas limitadas!", "www.{sigla}.com.br", "Programação sujeita a alterações",
    "Certificado de participação", "Acesse o QR Code", "Organização:", "#{sigla}{ano}",
]


@dataclass
class Renderizado:
    texto: str
    atividades: list[dict]  # rótulos, no schema da Fase 3
    layout: str
    ruidos: list[str] = field(default_factory=list)
    estilos: dict = field(default_factory=dict)


# --------------------------------------------------------------------------
# Formatação de datas e horas
# --------------------------------------------------------------------------

def _dt(s: str | None) -> datetime | None:
    if not s:
        return None
    return datetime.fromisoformat(s).replace(tzinfo=None)


def fmt_dia(d: datetime, estilo: str, idx: int) -> str:
    sem = DIAS_SEMANA[d.weekday()]
    return {
        "dd/mm": f"{d:%d/%m}",
        "sem_dd/mm": f"{sem}, {d:%d/%m}",
        "sem_dd/mm/aaaa": f"{sem} ({d:%d/%m/%Y})",
        "dd_de_mes": f"{d.day} de {MESES[d.month - 1]}",
        "dd_de_mes_aaaa": f"{d.day} de {MESES[d.month - 1]} de {d.year}",
        "dd_bullet_mes": f"{d.day} • {MESES[d.month - 1].capitalize()}",
        "dia_n": f"Dia {idx + 1} - {d:%d/%m}",
        "SEM_dd/mm/aa": f"{sem.upper()} - {d:%d/%m/%y}",
    }[estilo]


def fmt_hora(d: datetime, estilo: str) -> str:
    if estilo == "hh:mm":
        return f"{d:%H:%M}"
    if estilo == "hhhmm":
        return f"{d:%H}h{d:%M}"
    # "h" curto: 9h, 9h30
    return f"{d.hour}h" if d.minute == 0 else f"{d.hour}h{d:%M}"


def fmt_intervalo(ini: datetime, fim: datetime | None, estilo_h: str, estilo_i: str) -> str:
    a = fmt_hora(ini, estilo_h)
    if fim is None:
        return a
    b = fmt_hora(fim, estilo_h)
    return {
        "hifen": f"{a} - {b}",
        "travessao": f"{a} – {b}",
        "as": f"{a} às {b}",
        "das_as": f"das {a} às {b}",
        "parenteses": f"({a} - {b})",
    }[estilo_i]


def descricao_para_linhas(desc_html: str | None) -> list[str]:
    if not desc_html:
        return []
    s = re.sub(r"<br\s*/?>", "\n", desc_html)
    s = re.sub(r"</p>|<hr\s*/?>", "\n", s)
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return [re.sub(r"\s+", " ", ln).strip() for ln in s.splitlines() if ln.strip()]


# --------------------------------------------------------------------------
# Ruídos
# --------------------------------------------------------------------------

def _ocr(s: str, rng: random.Random, taxa: float = 0.04) -> str:
    out = []
    for ch in s:
        r = rng.random()
        if r < taxa / 3:
            continue  # caractere perdido
        if r < 2 * taxa / 3 and ch.isalpha():
            out.append({"o": "0", "l": "1", "i": "í", "a": "á", "e": "c", "m": "rn"}.get(ch, ch))
            continue
        out.append(ch)
        if r > 1 - taxa / 3:
            out.append(rng.choice([" ", "|", "*", "'"]))
    return "".join(out)


def _quebrar(nome: str, rng: random.Random) -> list[str]:
    if len(nome) < 40:
        return [nome]
    return textwrap.wrap(nome, width=rng.randint(22, 38), break_long_words=False) or [nome]


def _sigla(nome_evento: str) -> str:
    letras = "".join(w[0] for w in re.findall(r"[A-Za-zÀ-ú]+", nome_evento) if len(w) > 2)
    return (letras or "evento").lower()[:8]


# --------------------------------------------------------------------------
# Renderização
# --------------------------------------------------------------------------

def renderizar(evento: dict, layout: str, rng: random.Random, ruidos: list[str] | None = None) -> Renderizado:
    """`evento` = {"evento": {...}, "atividades": [...]} vindo do professor (já limpo)."""
    ruidos = list(ruidos or [])
    info = evento.get("evento", {}) or {}
    nome_evento = (info.get("nome") or "Programação").strip()
    acts = sorted(evento["atividades"], key=lambda a: (a["dataInicio"] or "", a["nome"]))
    ano = _dt(acts[0]["dataInicio"]).year if acts and acts[0]["dataInicio"] else datetime.now().year
    sigla = _sigla(nome_evento)

    estilos = {
        "dia": rng.choice(["dd/mm", "sem_dd/mm", "sem_dd/mm/aaaa", "dd_de_mes", "dd_de_mes_aaaa",
                           "dd_bullet_mes", "dia_n", "SEM_dd/mm/aa"]),
        "hora": rng.choice(["hh:mm", "hhhmm", "h"]),
        "intervalo": rng.choice(["hifen", "travessao", "as", "das_as", "parenteses"]),
        "sep_tabela": rng.choice([" | ", "\t"]),
        "maiusculas": layout == "cartaz" or rng.random() < 0.1,
    }

    def nome_txt(a):
        return a["nome"].upper() if estilos["maiusculas"] else a["nome"]

    rotulos = []
    for a in acts:
        r = {k: a.get(k) for k in ("nome", "lugar", "dataInicio", "dataFim", "descricao")}
        r["nome"] = nome_txt(a)
        if layout == "cartaz" and r["lugar"]:
            r["lugar"] = r["lugar"].upper()  # no cartaz o local também sai em caixa alta
        rotulos.append(r)

    linhas: list[str] = []

    # Cabeçalho: o ano SEMPRE aparece em algum lugar do texto (decisão da Fase 5),
    # porque o ano do rótulo precisa ser inferível do texto.
    cab = rng.choice([
        [f"{nome_evento} {ano}", "Programação"],
        [nome_evento, f"Programação {ano}"],
        [nome_evento.upper(), info.get("local_geral") or "", "PROGRAMAÇÃO"],
        [f"Programação - {nome_evento}", f"Edição {ano}"],
    ])
    linhas += [c for c in cab if c]
    if str(ano) not in "\n".join(linhas) and "aaaa" not in estilos["dia"]:
        linhas.append(rng.choice([f"© {ano} {nome_evento}", f"Inscrições até 10/01/{ano}", f"Edição {ano}"]))

    def decor():
        if "decorativo" in ruidos and rng.random() < 0.35:
            t = rng.choice(DECORATIVOS).format(sigla=sigla, ano=ano)
            linhas.append(_ocr(t, rng) if "ocr" in ruidos else t)

    def desc_linhas(a):
        ls = descricao_para_linhas(a.get("descricao"))
        return [_ocr(ln, rng, 0.02) for ln in ls] if "ocr" in ruidos else ls

    def nome_linhas(a):
        n = nome_txt(a)
        return _quebrar(n, rng) if "quebra" in ruidos else [n]

    # Só vira cabeçalho a seção que agrupa 2+ atividades (seções de uma atividade
    # só repetiriam o nome dela e não são realistas).
    tamanho_secao = Counter(a.get("secao") for a in acts if a.get("secao"))

    dias = []
    for a in acts:
        d = _dt(a["dataInicio"]).date() if a["dataInicio"] else None
        if not dias or dias[-1][0] != d:
            dias.append((d, []))
        dias[-1][1].append(a)

    for idx, (dia, grupo) in enumerate(dias):
        linhas.append("")
        if dia is not None:
            linhas.append(fmt_dia(datetime.combine(dia, datetime.min.time()), estilos["dia"], idx))
        if layout == "tabela":
            sep = estilos["sep_tabela"]
            linhas.append(sep.join(["Horário", "Atividade", "Local", "Descrição"]))
        elif layout == "colunas":
            linhas += ["Horário", "Atividade", "Local"]
        secao_atual = None
        for a in grupo:
            if ("secoes" in ruidos and a.get("secao") and a["secao"] != secao_atual
                    and tamanho_secao[a["secao"]] >= 2):
                secao_atual = a["secao"]
                linhas.append(secao_atual.upper() if rng.random() < 0.5 else secao_atual)
            ini, fim = _dt(a["dataInicio"]), _dt(a.get("dataFim"))
            hora = fmt_intervalo(ini, fim, estilos["hora"], estilos["intervalo"]) if ini else ""
            lugar = a.get("lugar") or ""
            if layout == "lista":
                sep = rng.choice([" | ", " - ", "  ", "\n"])
                nl = nome_linhas(a)
                linhas.append(f"{hora}{sep}{nl[0]}" if hora else nl[0])
                linhas += nl[1:]
                if lugar:
                    linhas.append(rng.choice([f"Local: {lugar}", lugar, f"📍 {lugar}"]))
                linhas += desc_linhas(a)
            elif layout == "tabela":
                sep = estilos["sep_tabela"]
                linhas.append(sep.join([hora, nome_txt(a), lugar, " ".join(desc_linhas(a))]).rstrip(" |\t"))
            elif layout == "colunas":
                linhas.append(hora)
                linhas += nome_linhas(a)
                if lugar:
                    linhas.append(lugar)
                linhas += desc_linhas(a)
            else:  # cartaz
                linhas.append(hora)
                linhas += nome_linhas(a)
                linhas += desc_linhas(a)
                if lugar:
                    linhas.append(lugar.upper())
            decor()

    if "decorativo" in ruidos:
        linhas += ["", rng.choice(["Realização", "Apoio"]) + ":", f"@{sigla}"]

    texto = "\n".join(linhas).strip() + "\n"
    return Renderizado(texto=texto, atividades=rotulos, layout=layout, ruidos=ruidos, estilos=estilos)
