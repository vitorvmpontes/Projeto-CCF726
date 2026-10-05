# extraction/

Fase 1 do pipeline: converte o arquivo da programação em **texto bruto**.

| Formato | Extrator | Detalhe |
|---|---|---|
| PDF | `PDFExtractor` | PyMuPDF, `page.get_text("text")`, páginas concatenadas. Reproduz os textos do TCC. |
| Imagem (png, jpg, jpeg) | `ImageExtractor` | Google Vision REST, `TEXT_DETECTION`. Precisa de `GOOGLE_VISION_API_KEY` no `.env`. |
| HTML (htm, html) | `HTMLExtractor` | BeautifulSoup; remove `script`/`style`; uma linha por elemento de bloco. |
| Planilha (xlsx, xls) | `SpreadsheetExtractor` | Pandas; uma linha por linha da planilha, células separadas por ` \| ` (mantém as colunas). |

## Uso

```powershell
# texto de um arquivo qualquer
python -m extraction caminho\do\arquivo.pdf -o saida.txt

# gera os textos que faltam no conjunto de teste (nunca sobrescreve os existentes)
python -m extraction.build_test_raw_text --dry-run
python -m extraction.build_test_raw_text
```

Os textos de `data/test/raw_text/` estão **congelados**: são a entrada oficial de todos os modelos na avaliação. Só são regerados com `--force <id>`.

`legacy_tcc/` tem o código original da POC do TCC, só como referência.
