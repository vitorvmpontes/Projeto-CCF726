# data/test — Conjunto de teste (dataset do TCC)

**Uso exclusivo para avaliação final.** Nunca usar para treino, validação ou ajuste de prompt/hiperparâmetros.

| Pasta | Conteúdo | Origem |
|---|---|---|
| `files/` | Arquivos originais das programações (18) | repositório `dataset-extracao-eventos`, pasta `programações/` |
| `ground_truth/` | Anotação manual (17) | repositório `POC---Vitor-`, pasta `conjunto de validação/Manual/` |
| `baseline_gemini/` | Saídas do Gemini 2.0-Flash (temperatura 0, modo JSON) usadas no TCC (17) | repositório `POC---Vitor-`, pasta `conjunto de validação/IA/` |
| `raw_text/` | Textos brutos extraídos na fase 1 do pipeline (15 de 18) | repositório `POC---Vitor-`, pasta `textos/` |
| `manifest.csv` | Mapeamento id → evento, formato, arquivos, extrator e origem | — |

Os arquivos foram renomeados para `<evento>-<formato>`. O conteúdo não foi alterado.

## Versão do ground truth

Os gabaritos e as saídas do Gemini vêm do repositório de trabalho do TCC (`POC---Vitor-`), e **não** do repositório público `dataset-extracao-eventos`. Com esta versão, o script original (`evaluation/legacy_tcc/script1.py`) reproduz exatamente os números do artigo:

- P = 88,75%, R = 90,12%, F1 = 0,8943 (TP 292, FP 37, FN 32)

Alteração posterior: em 2026-09-29 foram corrigidos dois erros de digitação no gabarito `secom2024-img` ("PROMESSOR" → "PROMISSOR", "DESMISFICANDO" → "DESMISTIFICANDO"). Com isso, os números mudam em relação ao artigo. Os gabaritos ainda vão passar por uma revisão completa, com uma regra de anotação única.

A versão pública difere em 4 gabaritos (Bioeconomia, SECOM2024 imagem e PDF, WIT2025 dia 2) e em 1 saída do Gemini (Bioeconomia). Com ela, o mesmo script dá F1 ≈ 0,82.

## Textos brutos

- PDFs: PyMuPDF, `page.get_text("text")`, páginas concatenadas.
- Imagens: Google Vision `TEXT_DETECTION` (mantido também no extrator novo).
- **Pendentes** (a gerar com o extrator portado): `opmed-html` (BeautifulSoup), `secom2024-img` (OCR) e `secom2024-planilha` (Pandas).
- `secom2023-img` tem texto, mas não tem ground truth: não entra na avaliação.

## Observações

- 10 eventos, 18 arquivos, 17 avaliados.
- Somando os 17 ground truths, são 324 atividades. SECOM2024 aparece em 3 formatos, então são 268 atividades distintas.
- Campos ausentes no ground truth estão como `null`. O campo de local se chama `lugar` na maioria dos arquivos e `lugarId` em alguns, o que precisa de normalização na avaliação nova. O script original só lê `lugar`.
