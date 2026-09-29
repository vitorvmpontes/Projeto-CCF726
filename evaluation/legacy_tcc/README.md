# evaluation/legacy_tcc — Avaliação original do TCC

Scripts e relatórios usados no TCC, copiados sem alteração do repositório `POC---Vitor-` (`conjunto de validação/`). Servem de referência para reproduzir a baseline e portar a lógica para o script novo de avaliação.

| Arquivo | Descrição |
|---|---|
| `script1.py` | Script principal: detecção (P/R/F1 micro) e acurácia por campo. Casamento por `nome` com `lower().strip()`, emparelhamento guloso um-para-um. |
| `error_investigator.py` | Lista as divergências de campos de data para um evento. |
| `notebook.ipynb` | Tabelas de métricas a partir do CSV. |
| `relatorios/` | Saídas do `script1.py` (CSV/JSON) e relatórios parciais em texto (`errosData`, `relatorioParcial` etc.). |

Os caminhos no script são relativos (`../Manual`, `../IA`). Para rodá-lo aqui, aponte para `data/test/ground_truth` e `data/test/baseline_gemini`. Os arquivos precisam manter os mesmos nomes nas duas pastas, o que já é garantido pelo `manifest.csv`.

Limitações conhecidas, a tratar na avaliação nova:

- O campo `lugarId` não é comparado; só `lugar`.
- Datas são comparadas como string exata.
- A descrição é comparada por igualdade exata, depois de remover o HTML.
