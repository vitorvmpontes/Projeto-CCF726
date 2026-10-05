"""Extratores de texto bruto (fase 1 do pipeline).

Cada extrator recebe o caminho de um arquivo de programação e devolve uma
string de texto bruto. A escolha do extrator é feita por extensão em
`get_extractor` / `extract_text`.

Decisões (ver docs/PLANEJAMENTO.md):
- PDF: PyMuPDF, `page.get_text("text")`, páginas concatenadas sem separador.
  Reproduz byte a byte os textos do TCC em data/test/raw_text/.
- Imagem: Google Vision via REST, `TEXT_DETECTION` (mesmo modo do TCC).
- HTML: BeautifulSoup, com quebra de linha nos elementos de bloco.
- Planilha: Pandas, uma linha da planilha por linha de texto, células
  separadas por " | " (mantém a posição das colunas).
"""

from __future__ import annotations

import base64
import os
import re
from abc import ABC, abstractmethod
from datetime import datetime, time
from pathlib import Path

PDF_EXT = {".pdf"}
IMAGE_EXT = {".png", ".jpg", ".jpeg"}
HTML_EXT = {".html", ".htm"}
SHEET_EXT = {".xlsx", ".xls"}


class ExtractionError(RuntimeError):
    """Falha ao extrair texto de um arquivo."""


class BaseExtractor(ABC):
    name: str = "base"

    @abstractmethod
    def extract(self, path: str | Path) -> str: ...


class PDFExtractor(BaseExtractor):
    name = "PyMuPDF get_text('text')"

    def extract(self, path: str | Path) -> str:
        import pymupdf

        try:
            with pymupdf.open(path) as doc:
                return "".join(page.get_text("text") for page in doc)
        except Exception as e:  # noqa: BLE001
            raise ExtractionError(f"Falha ao ler PDF '{path}': {e}") from e


class ImageExtractor(BaseExtractor):
    """OCR com a Google Cloud Vision API (REST + chave de API)."""

    name = "Google Vision (TEXT_DETECTION)"
    URL = "https://vision.googleapis.com/v1/images:annotate"

    def __init__(self, api_key: str | None = None, timeout: int = 60):
        self.api_key = api_key or os.getenv("GOOGLE_VISION_API_KEY")
        self.timeout = timeout
        if not self.api_key:
            raise ExtractionError(
                "GOOGLE_VISION_API_KEY não definida. Preencha a variável no .env."
            )

    def extract(self, path: str | Path) -> str:
        import requests

        content = base64.b64encode(Path(path).read_bytes()).decode("ascii")
        payload = {
            "requests": [
                {"image": {"content": content}, "features": [{"type": "TEXT_DETECTION"}]}
            ]
        }
        resp = requests.post(
            self.URL, params={"key": self.api_key}, json=payload, timeout=self.timeout
        )
        if resp.status_code != 200:
            raise ExtractionError(
                f"Vision API respondeu {resp.status_code} para '{path}': {resp.text[:300]}"
            )
        result = resp.json()["responses"][0]
        if "error" in result:
            raise ExtractionError(f"Vision API: {result['error']}")
        annotations = result.get("textAnnotations") or []
        return annotations[0]["description"] if annotations else ""


class HTMLExtractor(BaseExtractor):
    name = "BeautifulSoup (blocos em linhas)"

    BLOCK_TAGS = {
        "address", "article", "aside", "blockquote", "dd", "div", "dl", "dt",
        "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5",
        "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre", "section",
        "table", "tbody", "td", "tfoot", "th", "thead", "tr", "ul",
    }
    DROP_TAGS = ["script", "style", "noscript", "svg", "template", "iframe"]

    def extract(self, path: str | Path) -> str:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(Path(path).read_bytes(), "lxml")
        for tag in soup(self.DROP_TAGS):
            tag.decompose()
        for br in soup.find_all("br"):
            br.replace_with("\n")
        for tag in soup.find_all(self.BLOCK_TAGS):
            tag.insert_before("\n")
            tag.insert_after("\n")
        lines = (
            re.sub(r"[ \t ]+", " ", line).strip()
            for line in soup.get_text("").splitlines()
        )
        return "\n".join(line for line in lines if line)


class SpreadsheetExtractor(BaseExtractor):
    name = "Pandas (linhas, células separadas por ' | ')"

    @staticmethod
    def _fmt(value) -> str:
        import pandas as pd

        try:
            if value is None or pd.isna(value):
                return ""
        except (TypeError, ValueError):
            pass
        if isinstance(value, datetime):
            if value.time() == time(0, 0):
                return value.strftime("%d/%m/%Y")
            return value.strftime("%d/%m/%Y %H:%M")
        if isinstance(value, time):
            return value.strftime("%H:%M")
        return re.sub(r"\s+", " ", str(value)).strip()

    def extract(self, path: str | Path) -> str:
        import pandas as pd

        try:
            sheets = pd.read_excel(path, sheet_name=None, header=None, dtype=object)
        except Exception as e:  # noqa: BLE001
            raise ExtractionError(f"Falha ao ler planilha '{path}': {e}") from e

        out: list[str] = []
        for sheet_name, df in sheets.items():
            if len(sheets) > 1:
                out.append(f"# {sheet_name}")
            for _, row in df.iterrows():
                cells = [self._fmt(v) for v in row.tolist()]
                while cells and not cells[-1]:
                    cells.pop()
                if any(cells):
                    out.append(" | ".join(cells))
        return "\n".join(out)


def get_extractor_class(path: str | Path) -> type[BaseExtractor]:
    ext = Path(path).suffix.lower()
    if ext in PDF_EXT:
        return PDFExtractor
    if ext in IMAGE_EXT:
        return ImageExtractor
    if ext in HTML_EXT:
        return HTMLExtractor
    if ext in SHEET_EXT:
        return SpreadsheetExtractor
    raise ExtractionError(f"Formato não suportado: '{ext}' ({path})")


def get_extractor(path: str | Path, **kwargs) -> BaseExtractor:
    return get_extractor_class(path)(**kwargs)


def extract_text(path: str | Path, **kwargs) -> str:
    """Extrai o texto bruto de um arquivo, escolhendo o extrator pela extensão."""
    return get_extractor(path, **kwargs).extract(path)
