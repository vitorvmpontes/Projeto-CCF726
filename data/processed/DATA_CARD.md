# Data card — dataset de treino/validação (fonte B: sintético)

Gerado em 2026-10-22T19:37:13+00:00 por `python -m dataset_builder.build montar`.

## Como foi construído

1. Especificações de eventos sorteadas (`dataset_builder/spec.py`): tipo, cidade, ano, dias, número de atividades e casos difíceis.
2. O professor (Gemini) inventa cada evento já no formato do gabarito (`dataset_builder/teacher.py`).
3. O código renderiza cada evento como texto bruto, em layouts e com ruídos variados (`dataset_builder/render.py`). Como o texto vem do rótulo, o rótulo é correto por construção.
4. Filtros (`dataset_builder/filters.py`): schema, ancoragem (nome e local presentes no texto), datas (ano inferível do texto, fim ≥ início), tamanho e vazamento (nomes parecidos com os do conjunto de teste).
5. Divisão treino/validação **por evento** (`val` = 0.15).

## Números

| | |
|---|---|
| Eventos gerados | 500 |
| Eventos aprovados | 498 |
| Exemplos de treino | 845 (14024 atividades) |
| Exemplos de validação | 150 (2686 atividades) |
| Exemplos com nomes em CAIXA ALTA | 365 (37%) |
| Tokens estimados (p50 / p95 / máx.) | 2378 / 5261 / 6962 |

### Rejeições

| Motivo | Quantidade |
|---|---|
| muito_longo | 5 |

### Layouts

| Layout | Exemplos |
|---|---|
| cartaz | 275 |
| tabela | 256 |
| lista | 240 |
| colunas | 224 |

### Ruídos

| Ruído | Exemplos |
|---|---|
| quebra | 502 |
| secoes | 494 |
| decorativo | 418 |
| ocr | 243 |

## Limitações conhecidas

- Texto renderizado por código: mais regular que programações reais. A fonte A (crawler + professor) entra para compensar.
- O ano sempre aparece em algum lugar do texto (decisão da Fase 5), para o rótulo ser inferível.
- Grades com horários separados dos nomes (como a SECOM2024) não são geradas, porque a associação horário→atividade seria impossível a partir do texto.
- O conjunto de teste (`data/test/`) nunca é usado aqui, exceto pelo filtro de vazamento, que o compara para excluir exemplos parecidos.
