# data/

| Pasta | Conteúdo | Versionado |
|---|---|---|
| `raw/` | Arquivos originais coletados pelo crawler (cópia local; a fonte oficial é o S3) | Não |
| `interim/` | Textos extraídos dos arquivos coletados | Não |
| `processed/` | `train.jsonl` e `val.jsonl` | Sim |
| `test/files/` | Arquivos originais do dataset do TCC | Sim |
| `test/raw_text/` | Textos brutos congelados do teste (entrada de todos os modelos) | Sim |
| `test/ground_truth/` | JSONs anotados do TCC | Sim |

O conjunto `test/` é usado **somente** na avaliação final. Nunca use esses dados para treino ou validação.
