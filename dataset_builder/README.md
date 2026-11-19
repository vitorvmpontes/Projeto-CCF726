# dataset_builder/

Construção do dataset de treino e validação (Fase 5). Só a **fonte B (sintética)**: dados reais (crawler + professor) ficaram para trabalho futuro, com a redução de escopo de 2026-11-16.

## Como funciona

```
spec.py      sorteia especificações de eventos (tipo, cidade, ano, dias, nº de atividades, casos difíceis, estilo)
   ↓
teacher.py   o professor (gemini-3.8-flash) inventa o evento já no formato do gabarito
   ↓          → data/sintetico/eventos/<id>.json (versionado)
render.py    o código transforma cada evento em texto bruto: 4 layouts × ruídos × perfis
   ↓          (lista, tabela, colunas, cartaz) × (seções, decorativo, quebra de títulos, OCR)
   ↓          × (completo, sem_lugar, sem_descricao, enxuto)
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

# 3. versão 1.1: +300 eventos no estilo enxuto (semente 43) e perfis de renderização
python -m dataset_builder.build gerar --n-eventos 300 --semente 43 --estilo enxuto
python -m dataset_builder.build montar --por-evento 2 --val 0.15
```

### Perfis e estilos (v1.1)

Nas programações reais, a falta de local e de descrição costuma valer para o **documento inteiro**: no teste, 8 dos 17 arquivos não informam local de nenhuma atividade e 7 não têm descrição em nenhuma. Na v1, nenhum texto era assim. Duas mudanças:

- **Perfil de renderização** (`render.py`): cada texto sorteia `completo` (40%), `sem_lugar` (20%), `sem_descricao` (10%) ou `enxuto` (30%). O perfil apaga o campo do texto **e** do rótulo, então o rótulo continua correto. Custo zero.
- **Estilo do evento** (`spec.py` + `teacher.py`): `--estilo enxuto` pede ao professor programações curtas (2 a 6 atividades por dia, nomes diretos, quase sem descrição), como posts e cartazes. Dá diversidade de eventos, não só de renderização.

`montar --sem-perfis` renderiza tudo no perfil `completo`, como a v1.

### Extras da v1.2 (exploratória, 2026-11-20)

Motivados pelos erros do teste da e2b-r1 (`evaluation/results/RESULTADO_E2B_R1.md`). Não exigem eventos novos: só mudam a renderização dos mesmos 800 eventos.

- Separadores " – " e ": " depois do horário (`16h30 às 17h – COFFEE BREAK`, `14h: ABERTURA`).
- `local_cabecalho` (35%): o local aparece uma vez, no topo (`Local: X`) ou no dia (`14 DE OUTUBRO – LOCAL – X`), e vale para todas as atividades sem local próprio, como nos gabaritos do teste.
- `data_no_titulo` (40%, só eventos de um dia): sem cabeçalho de dia; a data aparece só no título ou no rodapé.
- `aspas` (25%): títulos de palestras/mesas entre aspas tipográficas; o rótulo mantém as aspas.

`montar --sem-extras` gera como a v1.1.

O `gerar` pula eventos já gerados, então pode ser interrompido e retomado. Mesma semente → mesmas especificações.

## Formato de cada linha do JSONL

```json
{"id": "sint-42-00007-0", "evento_id": "sint-42-00007", "fonte": "sintetico",
 "layout": "colunas", "ruidos": ["secoes", "quebra"], "estilos": {...},
 "perfil": "sem_lugar", "estilo_evento": "detalhado",
 "tipo_evento": "...", "casos": [...], "modelo_professor": "gemini-3.8-flash",
 "n_atividades": 14, "tokens_estimados": 2310,
 "texto": "<texto bruto da programação>",
 "atividades": [{"nome": "...", "lugar": "...", "dataInicio": "...", "dataFim": null, "descricao": "<p>...</p>"}]}
```

`atividades` segue exatamente o schema da Fase 3 (`inference/schema.py`).
