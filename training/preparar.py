"""Prepara os dados do fine-tuning e da avaliação na validação.

1. Converte data/processed/{train,val}.jsonl para o formato de conversa
   (inference/prompt.py) → training/dados/{train,val}_chat.jsonl.
2. Monta a validação no MESMO formato do conjunto de teste, para usar
   evaluation/run_slm.py e evaluation/evaluate.py sem mudanças:
       data/val_eval/raw_text/<id>.txt
       data/val_eval/ground_truth/<id>.json
       data/val_eval/manifest.csv         (validação inteira)
       data/val_eval/manifest_rapido.csv  (amostra fixa, para avaliar cada rodada)

Uso (na raiz do repositório, no PC ou no Colab):
    python -m training.preparar
"""

from __future__ import annotations

import argparse
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

from inference.prompt import VERSAO_PROMPT, conversa_treino

PROCESSED = Path("data/processed")
DADOS = Path("training/dados")
VAL_EVAL = Path("data/val_eval")
CAMPOS_MANIFEST = ["id", "evento", "formato", "raw_text", "ground_truth", "avaliado", "perfil", "estilo_evento",
                   "modelo_professor"]


def ler(nome: str) -> list[dict]:
    return [json.loads(l) for l in (PROCESSED / f"{nome}.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]


def amostra_estratificada(exemplos: list[dict], n: int, semente: int) -> list[dict]:
    """Amostra por (estilo do evento, perfil), um texto por evento, proporcional ao tamanho de cada grupo."""
    rng = random.Random(semente)
    grupos: dict[tuple, list] = defaultdict(list)
    for e in sorted(exemplos, key=lambda e: e["id"]):
        grupos[(e.get("estilo_evento", "detalhado"), e.get("perfil", "completo"))].append(e)
    total = len(exemplos)
    escolhidos, eventos = [], set()
    for chave in sorted(grupos):
        g = grupos[chave][:]
        rng.shuffle(g)
        k = max(1, round(n * len(g) / total))
        for e in g:
            if len([x for x in escolhidos if (x.get("estilo_evento"), x.get("perfil")) == chave]) >= k:
                break
            if e["evento_id"] in eventos:
                continue
            eventos.add(e["evento_id"])
            escolhidos.append(e)
    return sorted(escolhidos, key=lambda e: e["id"])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n-rapido", type=int, default=60, help="exemplos da validação rápida")
    ap.add_argument("--semente", type=int, default=42)
    args = ap.parse_args()

    if not (PROCESSED / "train.jsonl").exists():
        print("ERRO: rode antes `python -m dataset_builder.build montar`", file=sys.stderr)
        return 1

    DADOS.mkdir(parents=True, exist_ok=True)
    for nome in ("train", "val"):
        exemplos = ler(nome)
        with (DADOS / f"{nome}_chat.jsonl").open("w", encoding="utf-8") as f:
            for e in exemplos:
                f.write(json.dumps({"id": e["id"], "versao_prompt": VERSAO_PROMPT,
                                    "messages": conversa_treino(e["texto"], e["atividades"])},
                                   ensure_ascii=False) + "\n")
        print(f"{DADOS / (nome + '_chat.jsonl')}: {len(exemplos)} conversas")

    val = ler("val")
    for sub in ("raw_text", "ground_truth"):
        (VAL_EVAL / sub).mkdir(parents=True, exist_ok=True)
    linhas = []
    for e in val:
        (VAL_EVAL / "raw_text" / f"{e['id']}.txt").write_text(e["texto"], encoding="utf-8")
        (VAL_EVAL / "ground_truth" / f"{e['id']}.json").write_text(
            json.dumps(e["atividades"], ensure_ascii=False, indent=1), encoding="utf-8")
        linhas.append({"id": e["id"], "evento": e["evento_id"], "formato": e["layout"],
                       "raw_text": f"raw_text/{e['id']}.txt", "ground_truth": f"ground_truth/{e['id']}.json",
                       "avaliado": "sim", "perfil": e.get("perfil", ""), "estilo_evento": e.get("estilo_evento", ""),
                       "modelo_professor": e.get("modelo_professor", "")})

    def gravar(nome: str, rows: list[dict]) -> None:
        with (VAL_EVAL / nome).open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS_MANIFEST)
            w.writeheader()
            w.writerows(rows)

    gravar("manifest.csv", linhas)
    ids_rapido = {e["id"] for e in amostra_estratificada(val, args.n_rapido, args.semente)}
    rapido = [r for r in linhas if r["id"] in ids_rapido]
    gravar("manifest_rapido.csv", rapido)
    print(f"{VAL_EVAL}/manifest.csv: {len(linhas)} exemplos | manifest_rapido.csv: {len(rapido)} exemplos "
          f"({sum(1 for e in val if e['id'] in ids_rapido and e.get('estilo_evento') == 'enxuto')} enxutos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
