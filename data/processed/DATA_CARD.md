# Data card — dataset de treino/validação (fonte B: sintético, v1.2)

Gerado em 2026-11-19T18:56:02+00:00 por `python -m dataset_builder.build montar`.

## Como foi construído

1. Especificações de eventos sorteadas (`dataset_builder/spec.py`): tipo, cidade, ano, dias, número de atividades, casos difíceis e estilo (detalhado ou enxuto).
2. O professor inventa cada evento já no formato do gabarito (`dataset_builder/teacher.py`): `gemini-3.8-flash` nos eventos detalhados (via API) e Claude (`claude-opus-5-5`, numa sessão do Cowork, com as mesmas regras do prompt) nos 300 eventos enxutos da v1.1.
3. O código renderiza cada evento como texto bruto, em layouts, ruídos e perfis variados (`dataset_builder/render.py`). O perfil apaga local e/ou descrição do texto e do rótulo ao mesmo tempo. Como o texto vem do rótulo, o rótulo é correto por construção.
4. Filtros (`dataset_builder/filters.py`): schema, ancoragem (nome e local presentes no texto), datas (ano inferível do texto, fim ≥ início), tamanho e vazamento (nomes parecidos com os do conjunto de teste).
5. Divisão treino/validação **por evento** (`val` = 0.15).

## Números

| | |
|---|---|
| Eventos gerados | 800 |
| Eventos aprovados | 799 |
| Exemplos de treino | 1356 (17489 atividades) |
| Exemplos de validação | 240 (2686 atividades) |
| Exemplos com nomes em CAIXA ALTA | 488 (31%) |
| Tokens estimados (p50 / p95 / máx.) | 939 / 4221 / 6942 |

### Estilos de evento e perfis de renderização

| Professor | Exemplos |
|---|---|
| gemini-3.8-flash | 996 |
| claude-opus-5-5 (Cowork) | 600 |

| Estilo do evento | Exemplos |
|---|---|
| detalhado | 996 |
| enxuto | 600 |

| Perfil | Exemplos |
|---|---|
| completo | 672 |
| enxuto | 428 |
| sem_lugar | 309 |
| sem_descricao | 187 |

| Extra (v1.2) | Exemplos |
|---|---|
| local_cabecalho | 268 |
| data_no_titulo | 195 |
| aspas | 11 |

### Campos ausentes

| | Fração |
|---|---|
| atividades_sem_lugar | 0.433 |
| atividades_sem_descricao | 0.601 |
| atividades_sem_fim | 0.11 |
| textos_sem_nenhum_lugar | 0.405 |
| textos_sem_nenhuma_descricao | 0.547 |

### Rejeições

| Motivo | Quantidade |
|---|---|
| muito_longo | 3 |
| rotulo_muda_no_pos_processamento | 1 |

### Layouts

| Layout | Exemplos |
|---|---|
| lista | 442 |
| colunas | 391 |
| tabela | 383 |
| cartaz | 380 |

### Ruídos

| Ruído | Exemplos |
|---|---|
| quebra | 816 |
| secoes | 786 |
| decorativo | 624 |
| ocr | 401 |

## Qualidade dos rótulos

Avaliada por LLM como juiz (claude-opus-5-5 (Cowork)) numa amostra de 80 exemplos (923 atividades), metade de cada professor, com os critérios de `data/test/ANOTACAO.md`. Detalhes em `data/processed/revisao/JUIZ.md`.

| | |
|---|---|
| Atividades com erro | 2 de 923 (0.2%) |
| Vereditos | ok: 921, campo: 1, irreal: 1 |
| Erros — gemini-3.8-flash | 0 de 646 |
| Erros — claude-opus-5-5 (Cowork) | 2 de 277 |
| Conferência humana dos vereditos | 20 de 20 concordam (100%) |

Os erros encontrados vinham do renderizador (fim em outro dia sem data no texto; perfil que apagava o local e criava duplicatas) e foram corrigidos antes da versão final. O juiz é o mesmo modelo que gerou os eventos enxutos, o que pode torná-lo complacente com eles; por isso a conferência humana.

## Limitações conhecidas

- Só dados sintéticos: o texto é renderizado por código e é mais regular que programações reais. Dados reais (crawler + professor) ficaram para trabalho futuro.
- Os pesos dos perfis foram calibrados pela proporção agregada de programações sem local/descrição no conjunto de teste (nenhum texto nem rótulo do teste é usado).
- O ano sempre aparece em algum lugar do texto (decisão da Fase 5), para o rótulo ser inferível.
- Grades com horários separados dos nomes (como a SECOM2024) não são geradas, porque a associação horário→atividade seria impossível a partir do texto.
- O conjunto de teste (`data/test/`) nunca é usado aqui, exceto pelo filtro de vazamento, que o compara para excluir exemplos parecidos.
