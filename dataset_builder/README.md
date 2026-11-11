# dataset_builder/

Construção do dataset de treino e validação (Fase 5). Por enquanto só a **fonte B (sintética)**. A fonte A (crawler + professor) entra no mesmo pipeline depois da Fase 4.

## Como funciona

```
spec.py      sorteia especificações de eventos (tipo, cidade, ano, dias, nº de atividades, casos difíceis)
   ↓
teacher.py   o professor (gemini-3.8-flash) inventa o evento já no formato do gabarito
   ↓          → data/sintetico/eventos/<id>.json (versionado)
render.py    o código transforma cada evento em texto bruto: 4 layouts × ruídos
   ↓          (lista, tabela, colunas, cartaz) × (seções, decorativo, quebra de títulos, OCR)
filters.py   schema · ancoragem · datas · tamanho · vazamento para o teste
   ↓
build.py     divisão por EVENTO → data/processed/{train,val}.jsonl + estatisticas.json + DATA_CARD.md
```

**O texto vem do rótulo, e não o contrário.** O LLM nunca escreve a programação; quem escreve é o código. Por isso o rótulo é correto por construção, e toda informação da descrição está no texto.

## Uso

```powershell
# 1. piloto: 10 eventos (centavos de dólar), para conferir a qualidade
python -m dataset_builder.build gerar --n-eventos 10
python -m dataset_builder.build montar

# 2. versão 1: 500 eventos × 2 textos ≈ 1.000 exemplos
python -m dataset_builder.build gerar --n-eventos 500
python -m dataset_builder.build montar --por-evento 2 --val 0.15
```

O `gerar` pula eventos já gerados, então pode ser interrompido e retomado. Mesma semente → mesmas especificações.

## Formato de cada linha do JSONL

```json
{"id": "sint-42-00007-0", "evento_id": "sint-42-00007", "fonte": "sintetico",
 "layout": "colunas", "ruidos": ["secoes", "quebra"], "estilos": {...},
 "tipo_evento": "...", "casos": [...], "modelo_professor": "gemini-3.8-flash",
 "n_atividades": 14, "tokens_estimados": 2310,
 "texto": "<texto bruto da programação>",
 "atividades": [{"nome": "...", "lugar": "...", "dataInicio": "...", "dataFim": null, "descricao": "<p>...</p>"}]}
```

`atividades` segue exatamente o schema da Fase 3 (`inference/schema.py`).
