"""Testes dos extratores de texto (extraction/)."""

import csv
import re
from pathlib import Path

import pytest

from extraction.extractors import (
    ExtractionError, HTMLExtractor, ImageExtractor, PDFExtractor, SpreadsheetExtractor, get_extractor,
)

ROOT = Path(__file__).resolve().parents[1]
TEST_DIR = ROOT / "data" / "test"


def _rows(fmt):
    with (TEST_DIR / "manifest.csv").open(encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["formato"] == fmt and r["raw_text"]]


def _ws(s: str) -> str:
    return re.sub(r"[ \t]+", " ", s)


@pytest.mark.parametrize("row", _rows("pdf"), ids=lambda r: r["id"])
def test_pdf_reproduz_textos_congelados(row):
    """O extrator de PDF deve gerar o mesmo texto usado no TCC.

    A comparação ignora diferenças em sequências de espaços: versões do PyMuPDF
    podem variar nisso (ex.: secom2023-pdf tem um espaço a mais no texto do TCC).
    Os textos congelados em raw_text/ continuam sendo a entrada oficial."""
    frozen = (TEST_DIR / row["raw_text"]).read_text(encoding="utf-8")
    assert _ws(PDFExtractor().extract(TEST_DIR / row["arquivo"])) == _ws(frozen)


@pytest.mark.parametrize("fmt,cls", [("html", HTMLExtractor), ("planilha", SpreadsheetExtractor)])
def test_html_e_planilha_reproduzem_textos_congelados(fmt, cls):
    for row in _rows(fmt):
        frozen = (TEST_DIR / row["raw_text"]).read_text(encoding="utf-8")
        assert cls().extract(TEST_DIR / row["arquivo"]) == frozen


def test_roteamento_por_extensao(monkeypatch):
    monkeypatch.setenv("GOOGLE_VISION_API_KEY", "fake")
    assert isinstance(get_extractor("a.PDF"), PDFExtractor)
    assert isinstance(get_extractor("a.htm"), HTMLExtractor)
    assert isinstance(get_extractor("a.xlsx"), SpreadsheetExtractor)
    assert isinstance(get_extractor("a.jpeg"), ImageExtractor)
    with pytest.raises(ExtractionError):
        get_extractor("a.docx")


def test_imagem_sem_chave_falha_com_mensagem_clara(monkeypatch):
    monkeypatch.delenv("GOOGLE_VISION_API_KEY", raising=False)
    with pytest.raises(ExtractionError, match="GOOGLE_VISION_API_KEY"):
        ImageExtractor()
