"""Extrai o texto bruto de um arquivo qualquer.

Uso:
    python -m extraction <arquivo> [-o saida.txt]
"""

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

from .extractors import ExtractionError, extract_text


def main() -> int:
    load_dotenv()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("arquivo", type=Path)
    p.add_argument("-o", "--saida", type=Path, help="arquivo .txt de saída (padrão: imprime na tela)")
    args = p.parse_args()
    try:
        text = extract_text(args.arquivo)
    except ExtractionError as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 1
    if args.saida:
        args.saida.write_text(text, encoding="utf-8", newline="")
        print(f"Texto salvo em {args.saida} ({len(text)} caracteres)")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
