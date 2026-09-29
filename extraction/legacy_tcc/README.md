# extraction/legacy_tcc — Código da POC do TCC

Copiado sem alteração do repositório `POC---Vitor-` (`pipeline/` e `script/`). É a referência para portar a fase 1 (extração de texto).

| Arquivo | Descrição |
|---|---|
| `extractors.py` | `PDFExtractor` (PyMuPDF) e `ImageExtractor` (Google Vision via REST, `DOCUMENT_TEXT_DETECTION`) |
| `extrator.py` | Script avulso de PyMuPDF usado para gerar `data/test/raw_text/*-pdf.txt` |
| `main.py`, `llm_service.py`, `config.py` | Orquestração da POC com Gemini (`gemini-1.5-pro-latest`, temperatura 0,1) |
| `prompt.txt` | Prompt da POC |

Observações:

- A POC não tem extratores de HTML nem de planilha.
- Os textos das imagens em `data/test/raw_text/` foram gerados com `TEXT_DETECTION`, mas o `extractors.py` usa `DOCUMENT_TEXT_DETECTION`. **Decisão (2026-09-29):** o extrator portado usa `TEXT_DETECTION`, para manter a comparabilidade com a baseline.
- A POC foi só um teste. A configuração do Gemini dela (1.5-pro, temperatura 0,1, sem modo JSON) **não** é a da baseline. A baseline real (`data/test/baseline_gemini/`) foi gerada com o **Gemini 2.0-Flash**, temperatura 0 e modo JSON, no pipeline integrado ao myMobiConf.
