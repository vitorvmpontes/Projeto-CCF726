# Experimentos de fine-tuning

Uma linha por rodada. Mude **uma coisa por vez** em relação à rodada anterior e escreva qual foi em "Mudança".
As métricas de validação usam `data/val_eval/manifest_rapido.csv` (58 exemplos fixos) e `--pos-processar`.
O conjunto de teste só é usado no modelo final (Fase 8).

Configuração-base (rodada 1): QLoRA 4-bit, r = 16, alpha = 16, lr = 2e-4, 2 épocas, batch efetivo 8, warmup 5%, `adamw_8bit`, scheduler linear, semente 3407, prompt `v1`, template `gemma-4` sem thinking, melhor checkpoint pela loss no val.

| Rodada | Modelo | Mudança | Exemplos | Tempo (min) | Memória (GB) | Loss treino | Melhor loss val | F1 exato val | F1 aprox. val | JSON válido | Observações |
|---|---|---|---|---|---|---|---|---|---|---|---|
| e2b-r1 | Gemma 4 E2B | configuração-base (dados v1.1) | 1.348 (9 removidos > 8.192 tokens) | 188 | 11,9 | 0,0056 | 0,0021 (passo 294, ép. 1,74) | 100,0% (579/579) | 100,0% | 100% | Loss de validação estável desde ~1 época (0,0021 no passo 168); sem sobreajuste. Commit `dea4fe2`. GGUF do modelo inteiro estourou a RAM do Colab; avaliado com base `unsloth/gemma-4-E2B-it-GGUF` Q4_K_M + LoRA F16 no llama.cpp (RTX 3050), 24,5 s/exemplo. Val rápido (60 ex.) saturado: campos lugar 99,7%, dataInicio 100%, dataFim 99,7%, descrição 99,8% |

| e2b-r2 | Gemma 4 E2B | **exploratória**: dados v1.2 (extras motivados pelo teste) + 1 época | | | | | | | | | |

## Resultados no teste (17 arquivos do TCC)

O teste só é usado por rodadas pré-registradas ou, depois disso, marcadas como **exploratórias**. Arquivos completos em `treinamentos/t<n>/`.

| Rodada | Pós-proc. | Tipo | P | R | F1 exato | IC95 | F1 aprox. | JSON válido |
|---|---|---|---|---|---|---|---|---|
| Gemini 2.0-Flash (TCC) | v1 = v2 | referência | 89,36 | 90,74 | 90,05 | [84,55; 95,13] | 92,50 | 17/17 |
| **e2b-r1** | v1 | **principal (pré-registrada)** | 78,70 | 67,28 | **72,55** | [57,65; 84,78] | 81,20 | 16/17 |
| e2b-r1 | bruto | principal | 70,78 | 67,28 | 68,99 | [52,63; 83,73] | 77,22 | 16/17 |
| e2b-r1 | v2 | exploratória (só pós-processamento) | 82,31 | 70,37 | 75,87 | [61,11; 87,10] | 81,20 | 16/17 |
| e2b-r2 | v2 | exploratória | | | | | | |

## Como preencher

- Tempo, memória e losses: `MyDrive/ccf726/<rodada>/rodada.json`.
- F1 e JSON válido: saída do `python -m evaluation.evaluate ... --nome val/<rodada> --pos-processar` (resumo em `evaluation/results/val/<rodada>/resumo.json`).
- Curva de loss: `MyDrive/ccf726/<rodada>/curva_loss.png`. Os arquivos de cada rodada (`rodada.json`, `log_treino.csv`, `curva_loss.png`) ficam em `treinamentos/t<n>/`.
