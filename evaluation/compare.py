"""Monta uma tabela comparativa (Markdown) a partir de pastas de resultados.

Uso:
    python -m evaluation.compare gemini-2.0-flash-tcc gemini-3.6-flash-low gemini-3.5-flash-lite-minimal
    python -m evaluation.compare --todos -o evaluation/results/BASELINE.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

RESULTS = Path("evaluation/results")


def _pct(v):
    return "—" if v is None else f"{100 * v:.2f}"


def _load(nome: str) -> dict:
    d = RESULTS / nome
    out = {"nome": nome}
    if (d / "resumo.json").exists():
        out["q"] = json.loads((d / "resumo.json").read_text(encoding="utf-8"))
    if (d / "eficiencia.json").exists():
        out["e"] = json.loads((d / "eficiencia.json").read_text(encoding="utf-8"))
    return out


def tabela(nomes: list[str]) -> str:
    linhas = [
        "## Qualidade (17 arquivos)",
        "",
        "| Experimento | P | R | F1 | IC95 F1 | F1 aprox. | Lugar | Data início | Data fim | Descrição | JSON válido | Schema |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    efic = [
        "## Eficiência",
        "",
        "| Experimento | Latência mediana (s) | Latência p95 (s) | Tokens/s | Tokens entrada | Tokens saída | Tokens raciocínio | Custo por programação (USD) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    tem_efic = False
    for nome in nomes:
        r = _load(nome)
        q = r.get("q")
        if q:
            ex, ap, v = q["exato"], q["aproximado"], q["validade"]
            ic = ex.get("ic95_bootstrap", {}).get("f1")
            ic_txt = f"[{_pct(ic[0])}, {_pct(ic[1])}]" if ic else "—"
            acc = ex["acuracia_campos"]
            linhas.append(
                f"| {nome} | {_pct(ex['precisao'])} | {_pct(ex['revocacao'])} | **{_pct(ex['f1'])}** | {ic_txt} | "
                f"{_pct(ap['f1'])} | {_pct(acc['lugar'])} | {_pct(acc['dataInicio'])} | {_pct(acc['dataFim'])} | "
                f"{_pct(acc['descricao'])} | {_pct(v['json_valido'])} | {_pct(v['atividades_no_schema'])} |"
            )
        e = r.get("e")
        if e:
            tem_efic = True
            lat, tok, c = e["latencia_s"], e["tokens_medios"], e["custo_usd"]
            f = lambda x, n=2: "—" if x is None else f"{x:.{n}f}"  # noqa: E731
            efic.append(
                f"| {nome} | {f(lat['mediana'])} | {f(lat['p95'])} | {f(e['tokens_por_s_medio'], 1)} | "
                f"{f(tok['entrada'], 0)} | {f(tok['saida'], 0)} | {f(tok['raciocinio'], 0)} | {f(c['por_programacao'], 5)} |"
            )
    out = "\n".join(linhas)
    if tem_efic:
        out += "\n\n" + "\n".join(efic)
    return out + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("nomes", nargs="*")
    ap.add_argument("--todos", action="store_true", help="usa todas as pastas em evaluation/results")
    ap.add_argument("-o", "--saida", type=Path)
    args = ap.parse_args()
    nomes = sorted(p.name for p in RESULTS.iterdir() if p.is_dir()) if args.todos else args.nomes
    if not nomes:
        ap.error("informe os experimentos ou use --todos")
    md = tabela(nomes)
    if args.saida:
        args.saida.write_text(md, encoding="utf-8")
        print(f"Tabela salva em {args.saida}")
    sys.stdout.reconfigure(encoding="utf-8")
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
