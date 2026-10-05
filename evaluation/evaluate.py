"""Avalia um conjunto de predições contra o gabarito do conjunto de teste.

Lê data/test/manifest.csv, carrega para cada arquivo avaliado o gabarito
(`ground_truth/<id>.json`) e a predição (`<pred-dir>/<id>.json`) e calcula:

- Nível 1  (exato):      P/R/F1 micro, casamento por nome como no TCC
- Nível 1b (aproximado): P/R/F1 micro, casamento por similaridade >= limiar
- Nível 2:               acurácia por campo nos pares emparelhados
- Validade:              % de arquivos com JSON válido e % de atividades no schema
- IC 95% por bootstrap (reamostragem de arquivos) para P/R/F1

Uso (na raiz do repositório):
    python -m evaluation.evaluate --pred-dir data/test/baseline_gemini --nome gemini-2.0-flash
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from .loading import load_activities
from .metrics import FIELDS, Counts, evaluate_pair

MODES = ("exato", "aproximado")


def bootstrap_ci(per_file: list[Counts], n: int = 2000, seed: int = 42, alpha: float = 0.05) -> dict:
    """IC por bootstrap percentil, reamostrando arquivos com reposição e
    recalculando as métricas micro a cada reamostra."""
    if not per_file or n <= 0:
        return {}
    rng = np.random.default_rng(seed)
    arr = np.array([[c.tp, c.fp, c.fn] for c in per_file], dtype=float)
    idx = rng.integers(0, len(arr), size=(n, len(arr)))
    tp, fp, fn = (arr[idx].sum(axis=1)).T
    with np.errstate(divide="ignore", invalid="ignore"):
        p = np.where(tp + fp > 0, tp / (tp + fp), 0.0)
        r = np.where(tp + fn > 0, tp / (tp + fn), 0.0)
        f1 = np.where(p + r > 0, 2 * p * r / (p + r), 0.0)
    lo, hi = 100 * alpha / 2, 100 * (1 - alpha / 2)
    return {
        name: [float(np.percentile(v, lo)), float(np.percentile(v, hi))]
        for name, v in (("precisao", p), ("revocacao", r), ("f1", f1))
    }


def run(manifest: Path, pred_dir: Path, fuzzy_threshold: float, n_boot: int, seed: int) -> dict:
    base = manifest.parent
    with manifest.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("avaliado") == "sim"]

    per_file = []
    totals = {m: Counts() for m in MODES}
    files_json_ok = acts_total = acts_schema_ok = 0

    for r in rows:
        gt = load_activities(base / r["ground_truth"])
        if not gt.json_valid:
            raise SystemExit(f"Gabarito inválido para {r['id']}: {gt.error}")
        pred = load_activities(pred_dir / f"{r['id']}.json")

        res = evaluate_pair(gt.activities, pred.activities, fuzzy_threshold)
        for m in MODES:
            totals[m] = totals[m] + res[m]
        files_json_ok += pred.json_valid
        acts_total += pred.n_total
        acts_schema_ok += pred.schema_valid

        per_file.append({
            "id": r["id"], "evento": r["evento"], "formato": r["formato"],
            "n_gabarito": len(gt.activities), "n_predicao": len(pred.activities),
            "json_valido": pred.json_valid, "erro": pred.error,
            "schema_validas": pred.schema_valid, "schema_erros": pred.schema_errors[:5],
            **{m: res[m] for m in MODES},
        })

    def summary(c: Counts, files: list[Counts]) -> dict:
        return {
            "tp": c.tp, "fp": c.fp, "fn": c.fn,
            "precisao": c.precision, "revocacao": c.recall, "f1": c.f1,
            "ic95_bootstrap": bootstrap_ci(files, n_boot, seed),
            "acuracia_campos": c.field_accuracy(),
        }

    return {
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "predicoes": str(pred_dir.as_posix()),
        "manifest": str(manifest.as_posix()),
        "arquivos_avaliados": len(rows),
        "limiar_aproximado": fuzzy_threshold,
        "bootstrap": {"reamostras": n_boot, "semente": seed},
        "validade": {
            "json_valido": files_json_ok / len(rows) if rows else 0.0,
            "atividades_no_schema": acts_schema_ok / acts_total if acts_total else 0.0,
        },
        **{m: summary(totals[m], [f[m] for f in per_file]) for m in MODES},
        "_por_arquivo": per_file,
    }


def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    per_file = result.pop("_por_arquivo")
    (out_dir / "resumo.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")

    header = ["id", "evento", "formato", "n_gabarito", "n_predicao", "json_valido", "schema_validas"]
    for m in MODES:
        header += [f"{m}_{k}" for k in ("tp", "fp", "fn", "precisao", "revocacao", "f1")]
        header += [f"{m}_acc_{f}" for f in FIELDS]
    with (out_dir / "por_arquivo.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        for pf in per_file:
            row = [pf[k] for k in header[:7]]
            for m in MODES:
                c: Counts = pf[m]
                row += [c.tp, c.fp, c.fn, round(c.precision, 4), round(c.recall, 4), round(c.f1, 4)]
                row += [round(v, 4) for v in c.field_accuracy().values()]
            w.writerow(row)
    erros = {pf["id"]: pf["schema_erros"] or pf["erro"] for pf in per_file if pf["schema_erros"] or pf["erro"]}
    if erros:
        (out_dir / "erros_formato.json").write_text(json.dumps(erros, ensure_ascii=False, indent=2), encoding="utf-8")
    result["_por_arquivo"] = per_file


def print_report(result: dict, nome: str) -> None:
    pct = lambda v: f"{100 * v:6.2f}%"  # noqa: E731
    print(f"\n=== {nome} — {result['arquivos_avaliados']} arquivos ===")
    print(f"{'arquivo':<26}{'fmt':<9}{'GT':>4}{'Pred':>5}  {'P':>7} {'R':>7} {'F1':>7}  | F1 aprox")
    for pf in result["_por_arquivo"]:
        c, a = pf["exato"], pf["aproximado"]
        print(f"{pf['id']:<26}{pf['formato']:<9}{pf['n_gabarito']:>4}{pf['n_predicao']:>5}  "
              f"{pct(c.precision)} {pct(c.recall)} {pct(c.f1)}  | {pct(a.f1)}")
    for m, titulo in (("exato", "Nível 1  (nome exato)"), ("aproximado", f"Nível 1b (aproximado ≥ {result['limiar_aproximado']})")):
        s = result[m]
        ic = s["ic95_bootstrap"]
        ic_txt = f"  IC95 F1 [{100*ic['f1'][0]:.2f}, {100*ic['f1'][1]:.2f}]" if ic else ""
        print(f"\n{titulo}: TP {s['tp']} FP {s['fp']} FN {s['fn']} | "
              f"P {pct(s['precisao'])} R {pct(s['revocacao'])} F1 {pct(s['f1'])}{ic_txt}")
        print("  Nível 2: " + "  ".join(f"{k} {pct(v)}" for k, v in s["acuracia_campos"].items()))
    v = result["validade"]
    print(f"\nValidade: JSON válido {pct(v['json_valido'])} | atividades no schema {pct(v['atividades_no_schema'])}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--pred-dir", type=Path, required=True, help="pasta com <id>.json de cada predição")
    p.add_argument("--nome", required=True, help="nome do experimento (pasta de saída)")
    p.add_argument("--manifest", type=Path, default=Path("data/test/manifest.csv"))
    p.add_argument("--saida", type=Path, default=Path("evaluation/results"))
    p.add_argument("--limiar", type=float, default=0.9, help="similaridade mínima do Nível 1b (0-1)")
    p.add_argument("--bootstrap", type=int, default=2000, help="número de reamostras (0 desliga)")
    p.add_argument("--semente", type=int, default=42)
    args = p.parse_args()

    result = run(args.manifest, args.pred_dir, args.limiar, args.bootstrap, args.semente)
    print_report(result, args.nome)
    write_outputs(result, args.saida / args.nome)
    print(f"\nResultados salvos em {args.saida / args.nome}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
