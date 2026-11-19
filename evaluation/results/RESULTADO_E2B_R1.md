# Resultado no teste — e2b-r1 (Gemma 4 E2B + QLoRA)

Rodada pré-registrada em `docs/PLANEJAMENTO.md` (2026-11-19). Teste executado **uma vez**, em 2026-11-19, com o
`llama-server` (base `gemma-4-E2B-it-Q4_K_M.gguf` + LoRA `e2b-r1-lora.F16.gguf`, contexto 16k, temperatura 0, saída livre)
numa RTX 3050. Mesmos textos congelados (`data/test/raw_text/`) e mesmo script de avaliação da baseline.

## Números

| Modelo | P | R | **F1 exato** | IC95 F1 | F1 aprox. | lugar | início | fim | descrição | JSON válido |
|---|---|---|---|---|---|---|---|---|---|---|
| Gemini 2.0-Flash (TCC) | 89,36 | 90,74 | **90,05** | [84,55; 95,13] | 92,50 | 74,1 | 65,0 | 59,2 | 87,1 | 100% |
| gemini-3.6-flash (low) | 85,31 | 84,26 | 84,78 | [75,56; 92,68] | 88,51 | 70,3 | 73,3 | 68,5 | 84,6 | 100% |
| gemini-3.5-flash-lite (minimal) | 79,80 | 73,15 | 76,33 | [62,81; 88,08] | 83,74 | 51,9 | 71,7 | 65,8 | 12,7 | 100% |
| **e2b-r1** (com pós-processamento) | 78,70 | 67,28 | **72,55** | [57,65; 84,78] | 81,20 | 65,1 | 40,8 | 39,9 | 67,0 | 94% (16/17) |
| e2b-r1 (saída bruta) | 70,78 | 67,28 | 68,99 | [52,63; 83,73] | 77,22 | 65,1 | 40,4 | 39,9 | 67,0 | 94% |

Acurácia por campo nas atividades emparelhadas pelo nome exato. Latência: 43,6 s por programação em média (mediana 39 s), RTX 3050.
O pós-processamento descartou 54 datas inválidas e 31 atividades sem nome, e removeu 38 tags HTML não permitidas.

## Onde o SLM perde (TP 218 · FP 59 · FN 106; Gemini: 294 · 35 · 30)

1. **Grades com dias em colunas (SECOM 2024: pdf, planilha, img)** — 52 dos 106 FN. O dataset de treino exclui grades
   de propósito (decisão de 2026-10-21: a associação horário→atividade some na linearização). No `secom2024-pdf` o modelo
   entrou em loop ("Palestra", 23:00/23:30 repetidos) até o limite de 8.192 tokens e o JSON ficou incompleto (0 atividades).
   Sem os três arquivos da SECOM 2024: SLM F1 78,65 (aprox. 89,22) × Gemini 93,14 (aprox. 95,22).
2. **Diferenças de grafia no nome** — F1 exato 72,55 → aproximado 81,20. O modelo copia o texto ("–", aspas omitidas),
   enquanto o gabarito usa "-" e mantém as aspas tipográficas. Ex.: `forumcpa-pdf` F1 exato 47,4 × aproximado 89,5;
   `semanaacademicausp-pdf` 31,8 × 86,4. O Gemini tinha o mesmo problema, em menor grau (ver `ANALISE_BASELINE.md`).
3. **Datas** — início certo em 40,8% (Gemini 65,0%). Dois padrões: faixa de horário colada na data
   (`2018-08-13T08:40:00-09:00:00-03:00`, de "08h40 às 09h00 –") e só a hora, sem a data (`mannamuseu-pdf`: "10:30").
   Os dois formatos não aparecem no treino.
4. **Local geral do evento** — quando o local vem uma vez no cabeçalho ("Local: Auditório da Reitoria"), o gabarito do
   teste repete esse local em todas as atividades; o dataset sintético segue a convenção oposta (`null`). Divergência de
   convenção de anotação, não erro de leitura.
5. **Atividades a mais** em programações longas e soltas (`mannamuseu-pdf`: 48 previstas × 40 no gabarito).

## Leitura

A validação sintética saturou (F1 100%), mas o teste real ficou 17,5 pontos abaixo do Gemini 2.0. A diferença se
concentra em formatos e convenções que o gerador sintético não cobre (grades, faixas de horário, datas fora do bloco,
local no cabeçalho), e não na leitura de programações parecidas com as do treino: nos arquivos em lista/tabela simples
(MFP, SEBRAE, OPMED, WIT dia 3) o SLM fica perto do Gemini. É uma lacuna sintético→real, que reforça a necessidade
da fonte A (dados reais) adiada para 2027.
