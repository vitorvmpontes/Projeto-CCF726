"""Fase 1 do pipeline: extração de texto bruto das programações."""

from .extractors import ExtractionError, extract_text, get_extractor

__all__ = ["ExtractionError", "extract_text", "get_extractor"]
