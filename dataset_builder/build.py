"""Constrói o dataset de treino/validação (Fase 5).

Duas etapas:

1. `gerar` (usa a API do professor; roda no seu computador, com GEMINI_API_KEY):
       python -m dataset_builder.build gerar --n-eventos 500
   Sorteia as especificações, chama o professor e salva um JSON por evento em
   data/sintetico/eventos/. Eventos já gerados são pulados (dá para retomar).

3. `amostra`: sorteia exemplos para a revisão manual (data/processed/revisao/).

2. `montar` (sem API):
       python -m dataset_builder.build montar
   Limpa os eventos, renderiza cada um em N textos (layouts e ruídos
   sorteados), aplica os filtros, divide em treino/validação POR EVENTO e grava
   data/processed/train.jsonl, val.jsonl, estatisticas.json e DATA_CARD.md.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

from .filters import aplicar_filtros, estimar_tokens, limpar_evento
from .render import LAYOUTS, RUIDOS, renderizar
from .spec import EventoSpec, sortear_specs
from .teacher import MODELO_PADRAO, gerar_evento

EVENTOS_DIR = Path("data/sintetico/eventos")
SAIDA_DIR = Path("data/processed")
PRECO = {"entrada": 0.75, "saida": 3.75}  # gemini-3.8-flash, USD por 1M tokens (até 31/12/2026)


# --------------------------------------------------------------------------
# gerar
# --------------------------------------------------------------------------

def cmd_gerar(args) -> int:
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY"):
        print("ERRO: GEMINI_API_KEY não definida no .env", file=sys.stderr)
        return 1
    from google import genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    EVENTOS_DIR.mkdir(parents=True, exist_ok=True)
    specs = sortear_specs(args.n_eventos, args.semente)
    pendentes = [s for s in specs if not (EVENTOS_DIR / f"{s.id}.json").exists()]
    print(f"{len(specs)} especificações; {len(specs) - len(pendentes)} já geradas; {len(pendentes)} a gerar "
          f"com {args.modelo} ({args.workers} em paralelo)")

    uso_total = Counter()
    falhas = 0

    def tarefa(spec: EventoSpec):
        dados, uso = gerar_evento(client, spec, args.modelo)
        registro = {"spec": spec.to_dict(), "modelo": args.modelo,
                    "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "uso_tokens": uso, "saida": dados}
        (EVENTOS_DIR / f"{spec.id}.json").write_text(json.dumps(registro, ensure_ascii=False, indent=1), encoding="utf-8")
        return spec, uso

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(tarefa, s): s for s in pendentes}
        for k, fut in enumerate(as_completed(futs), 1):
            spec = futs[fut]
            try:
                _, uso = fut.result()
                uso_total.update(uso)
                custo = (uso_total["entrada"] * PRECO["entrada"] + uso_total["saida"] * PRECO["saida"]) / 1e6
                print(f"[{k}/{len(pendentes)}] {spec.id} ok  | custo acumulado ~US$ {custo:.2f}")
            except Exception as e:  # noqa: BLE001
                falhas += 1
                print(f"[{k}/{len(pendentes)}] {spec.id} FALHOU: {str(e)[:200]}")
    print(f"\nFim. Falhas: {falhas}. Rode de novo para tentar as que falharam.")
    return 0 if not falhas else 1


# --------------------------------------------------------------------------
# montar
# --------------------------------------------------------------------------

def _sortear_ruidos(rng: random.Random) -> list[str]:
    return [r for r in RUIDOS if rng.random() < {"secoes": 0.5, "decorativo": 0.4, "quebra": 0.5, "ocr": 0.25}[r]]


def cmd_montar(args) -> int:
    arquivos = sorted(EVENTOS_DIR.glob("*.json"))
    if not arquivos:
        print(f"Nenhum evento em {EVENTOS_DIR}. Rode primeiro: python -m dataset_builder.build gerar", file=sys.stderr)
        return 1
    rng = random.Random(args.semente)

    exemplos, rejeicoes, eventos_ok = [], Counter(), []
    for arq in arquivos:
        reg = json.loads(arq.read_text(encoding="utf-8"))
        evento, motivos = limpar_evento(reg["saida"])
        if evento is None:
            rejeicoes.update(motivos)
            continue
        eid = reg["spec"]["id"]
        layouts = rng.sample(LAYOUTS, k=min(args.por_evento, len(LAYOUTS)))
        aprovados = 0
        for k, layout in enumerate(layouts):
            r = renderizar(evento, layout, rng, _sortear_ruidos(rng))
            motivos = aplicar_filtros(r.texto, r.atividades)
            if motivos:
                rejeicoes.update(motivos)
                continue
            aprovados += 1
            exemplos.append({
                "id": f"{eid}-{k}", "evento_id": eid, "fonte": "sintetico",
                "layout": r.layout, "ruidos": r.ruidos, "estilos": r.estilos,
                "tipo_evento": reg["spec"]["tipo"], "casos": reg["spec"]["casos"],
                "modelo_professor": reg["modelo"],
                "n_atividades": len(r.atividades), "tokens_estimados": estimar_tokens(r.texto, r.atividades),
                "texto": r.texto, "atividades": r.atividades,
            })
        if aprovados:
            eventos_ok.append(eid)

    # divisão por evento: todos os textos de um evento ficam no mesmo split
    eventos_ok = sorted(set(eventos_ok))
    random.Random(args.semente).shuffle(eventos_ok)
    n_val = max(1, round(args.val * len(eventos_ok)))
    val_ids = set(eventos_ok[:n_val])
    train = [e for e in exemplos if e["evento_id"] not in val_ids]
    val = [e for e in exemplos if e["evento_id"] in val_ids]

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    for nome, dados in (("train", train), ("val", val)):
        with (SAIDA_DIR / f"{nome}.jsonl").open("w", encoding="utf-8") as f:
            for e in dados:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")

    stats = estatisticas(arquivos, train, val, rejeicoes, args)
    (SAIDA_DIR / "estatisticas.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    (SAIDA_DIR / "DATA_CARD.md").write_text(data_card(stats), encoding="utf-8")
    print(json.dumps({k: stats[k] for k in ("eventos_gerados", "exemplos", "rejeicoes")}, ensure_ascii=False, indent=2))
    print(f"\nArquivos em {SAIDA_DIR}/")
    return 0


def estatisticas(arquivos, train, val, rejeicoes, args) -> dict:
    todos = train + val

    def dist(chave):
        return dict(Counter(e[chave] for e in todos).most_common())

    toks = sorted(e["tokens_estimados"] for e in todos) or [0]
    return {
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "parametros": {"por_evento": args.por_evento, "val": args.val, "semente": args.semente},
        "eventos_gerados": len(arquivos),
        "eventos_aprovados": len({e["evento_id"] for e in todos}),
        "exemplos": {"train": len(train), "val": len(val), "total": len(todos)},
        "atividades": {"train": sum(e["n_atividades"] for e in train), "val": sum(e["n_atividades"] for e in val)},
        "rejeicoes": dict(rejeicoes.most_common()),
        "layouts": dist("layout"),
        "ruidos": dict(Counter(r for e in todos for r in e["ruidos"]).most_common()),
        "caixa_alta": {"exemplos": sum(1 for e in todos if e["estilos"].get("maiusculas")),
                       "fracao": round(sum(1 for e in todos if e["estilos"].get("maiusculas")) / len(todos), 3) if todos else 0},
        "tipos_evento": dist("tipo_evento"),
        "casos": dict(Counter(c for e in todos for c in e["casos"]).most_common()),
        "tokens_estimados": {"p50": toks[len(toks) // 2], "p95": toks[int(0.95 * (len(toks) - 1))], "max": toks[-1]},
    }


def data_card(s: dict) -> str:
    def tab(d):
        return "\n".join(f"| {k} | {v} |" for k, v in d.items())

    return f"""# Data card — dataset de treino/validação (fonte B: sintético)

Gerado em {s['gerado_em']} por `python -m dataset_builder.build montar`.

## Como foi construído

1. Especificações de eventos sorteadas (`dataset_builder/spec.py`): tipo, cidade, ano, dias, número de atividades e casos difíceis.
2. O professor (Gemini) inventa cada evento já no formato do gabarito (`dataset_builder/teacher.py`).
3. O código renderiza cada evento como texto bruto, em layouts e com ruídos variados (`dataset_builder/render.py`). Como o texto vem do rótulo, o rótulo é correto por construção.
4. Filtros (`dataset_builder/filters.py`): schema, ancoragem (nome e local presentes no texto), datas (ano inferível do texto, fim ≥ início), tamanho e vazamento (nomes parecidos com os do conjunto de teste).
5. Divisão treino/validação **por evento** (`val` = {s['parametros']['val']}).

## Números

| | |
|---|---|
| Eventos gerados | {s['eventos_gerados']} |
| Eventos aprovados | {s['eventos_aprovados']} |
| Exemplos de treino | {s['exemplos']['train']} ({s['atividades']['train']} atividades) |
| Exemplos de validação | {s['exemplos']['val']} ({s['atividades']['val']} atividades) |
| Exemplos com nomes em CAIXA ALTA | {s['caixa_alta']['exemplos']} ({100 * s['caixa_alta']['fracao']:.0f}%) |
| Tokens estimados (p50 / p95 / máx.) | {s['tokens_estimados']['p50']} / {s['tokens_estimados']['p95']} / {s['tokens_estimados']['max']} |

### Rejeições

| Motivo | Quantidade |
|---|---|
{tab(s['rejeicoes']) or '| — | 0 |'}

### Layouts

| Layout | Exemplos |
|---|---|
{tab(s['layouts'])}

### Ruídos

| Ruído | Exemplos |
|---|---|
{tab(s['ruidos'])}

## Limitações conhecidas

- Texto renderizado por código: mais regular que programações reais. A fonte A (crawler + professor) entra para compensar.
- O ano sempre aparece em algum lugar do texto (decisão da Fase 5), para o rótulo ser inferível.
- Grades com horários separados dos nomes (como a SECOM2024) não são geradas, porque a associação horário→atividade seria impossível a partir do texto.
- O conjunto de teste (`data/test/`) nunca é usado aqui, exceto pelo filtro de vazamento, que o compara para excluir exemplos parecidos.
"""


# --------------------------------------------------------------------------
# amostra para revisão manual
# --------------------------------------------------------------------------

def cmd_amostra(args) -> int:
    """Sorteia exemplos estratificados por layout e gera um Markdown para leitura
    e um CSV para registrar o veredito de cada atividade."""
    exemplos = [json.loads(l) for f in ("train.jsonl", "val.jsonl")
                for l in (SAIDA_DIR / f).read_text(encoding="utf-8").splitlines() if l.strip()]
    rng = random.Random(args.semente)
    por_layout: dict[str, list] = {}
    for e in exemplos:
        por_layout.setdefault(e["layout"], []).append(e)
    k = max(1, args.n // max(1, len(por_layout)))
    amostra = []
    usados = set()
    for layout in sorted(por_layout):
        cands = [e for e in por_layout[layout] if e["evento_id"] not in usados]
        for e in rng.sample(cands, min(k, len(cands))):
            usados.add(e["evento_id"])
            amostra.append(e)

    out = SAIDA_DIR / "revisao"
    out.mkdir(parents=True, exist_ok=True)
    md = ["# Revisão manual — amostra do dataset", "",
          f"{len(amostra)} exemplos ({k} por layout), semente {args.semente}. "
          "Para cada atividade, marque no `revisao.csv`: `ok` ou o tipo de erro.", "",
          "Tipos de erro: `nome_regra` (nome com subtítulo/palestrante/tema), `descricao` (informação errada, "
          "faltando ou inventada), `campo` (local/horário não confere com o texto), `irreal` (atividade ou texto "
          "implausível), `outro`.", ""]
    linhas_csv = []
    for e in amostra:
        md += [f"## {e['id']} — {e['layout']} — {e['tipo_evento']}", "",
               f"Ruídos: {', '.join(e['ruidos']) or 'nenhum'}", "", "### Texto", "", "```text", e["texto"].rstrip(), "```", "",
               "### Rótulo", "", "| # | nome | lugar | início | fim | descrição |", "|---|---|---|---|---|---|"]
        for i, a in enumerate(e["atividades"]):
            desc = (a["descricao"] or "").replace("|", "\\|")
            md.append(f"| {i} | {a['nome']} | {a['lugar'] or ''} | {(a['dataInicio'] or '')[:16]} | "
                      f"{(a['dataFim'] or '')[:16]} | {desc} |")
            linhas_csv.append([e["id"], i, a["nome"], "", ""])
        md.append("")
    (out / "AMOSTRA.md").write_text("\n".join(md), encoding="utf-8")
    import csv as _csv
    with (out / "revisao.csv").open("w", encoding="utf-8-sig", newline="") as f:
        w = _csv.writer(f, delimiter=";")
        w.writerow(["exemplo", "atividade", "nome", "veredito", "observacao"])
        w.writerows(linhas_csv)
    print(f"{len(amostra)} exemplos, {len(linhas_csv)} atividades -> {out}/AMOSTRA.md e revisao.csv")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    g = sub.add_parser("gerar", help="gera eventos com o professor (API)")
    g.add_argument("--n-eventos", type=int, default=500)
    g.add_argument("--modelo", default=MODELO_PADRAO)
    g.add_argument("--semente", type=int, default=42)
    g.add_argument("--workers", type=int, default=4)
    m = sub.add_parser("montar", help="renderiza, filtra e divide (sem API)")
    m.add_argument("--por-evento", type=int, default=2, help="textos renderizados por evento")
    m.add_argument("--val", type=float, default=0.15, help="fração de EVENTOS na validação")
    m.add_argument("--semente", type=int, default=42)
    a = sub.add_parser("amostra", help="gera a amostra para revisão manual")
    a.add_argument("--n", type=int, default=12, help="número de exemplos (dividido entre os layouts)")
    a.add_argument("--semente", type=int, default=7)
    args = p.parse_args()
    return {"gerar": cmd_gerar, "montar": cmd_montar, "amostra": cmd_amostra}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
