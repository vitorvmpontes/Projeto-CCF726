"""Gera e congela os textos brutos do conjunto de teste.

Para cada arquivo listado em data/test/manifest.csv que ainda não tem texto
em data/test/raw_text/, roda o extrator correspondente, salva
`raw_text/<id>.txt` e atualiza as colunas `raw_text` e `extrator_raw_text`
do manifest.

Textos já existentes NUNCA são sobrescritos (estão congelados), a menos que
se passe --force com ids explícitos.

Uso (na raiz do repositório):
    python -m extraction.build_test_raw_text            # gera só os faltantes
    python -m extraction.build_test_raw_text --dry-run  # mostra o que faria
    python -m extraction.build_test_raw_text --force opmed-html
"""

import argparse
import csv
import sys
from pathlib import Path

from dotenv import load_dotenv

from .extractors import ExtractionError, get_extractor, get_extractor_class

TEST_DIR = Path("data/test")
MANIFEST = TEST_DIR / "manifest.csv"


def main() -> int:
    load_dotenv()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--manifest", type=Path, default=MANIFEST)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--force", nargs="+", default=[], metavar="ID",
                   help="regera estes ids mesmo que o texto já exista")
    args = p.parse_args()

    base = args.manifest.parent
    with args.manifest.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = list(reader)

    falhas = 0
    for row in rows:
        out_rel = f"raw_text/{row['id']}.txt"
        out = base / out_rel
        if out.exists() and row["id"] not in args.force:
            if not row.get("raw_text"):  # texto existe mas o manifest não sabe
                row["raw_text"] = out_rel
                row["extrator_raw_text"] = get_extractor_class(base / row["arquivo"]).name
            continue
        src = base / row["arquivo"]
        try:
            extractor = get_extractor(src)
        except ExtractionError as e:
            print(f"[ERRO] {row['id']}: {e}")
            falhas += 1
            continue
        print(f"[{'dry-run' if args.dry_run else 'extraindo'}] {row['id']} <- {src.name} ({extractor.name})")
        if args.dry_run:
            continue
        try:
            text = extractor.extract(src)
        except ExtractionError as e:
            print(f"[ERRO] {row['id']}: {e}")
            falhas += 1
            continue
        out.write_text(text, encoding="utf-8", newline="")
        row["raw_text"] = out_rel
        row["extrator_raw_text"] = extractor.name
        print(f"         -> {out} ({len(text)} caracteres)")

    if not args.dry_run:
        with args.manifest.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    pendentes = [r["id"] for r in rows if not (base / f"raw_text/{r['id']}.txt").exists()]
    print(f"\nPendentes: {pendentes or 'nenhum'}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
