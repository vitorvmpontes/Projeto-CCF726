# Experimentos de fine-tuning

Uma linha por rodada. Mude **uma coisa por vez** em relação à rodada anterior e escreva qual foi em "Mudança".
As métricas de validação usam `data/val_eval/manifest_rapido.csv` (58 exemplos fixos) e `--pos-processar`.
O conjunto de teste só é usado no modelo final (Fase 8).

Configuração-base (rodada 1): QLoRA 4-bit, r = 16, alpha = 16, lr = 2e-4, 2 épocas, batch efetivo 8, warmup 5%, `adamw_8bit`, scheduler linear, semente 3407, prompt `v1`, template `gemma-4` sem thinking, melhor checkpoint pela loss no val.

| Rodada | Modelo | Mudança | Exemplos | Tempo (min) | Memória (GB) | Loss treino | Melhor loss val | F1 exato val | F1 aprox. val | JSON válido | Observações |
|---|---|---|---|---|---|---|---|---|---|---|---|
| e2b-r1 | Gemma 4 E2B | configuração-base | | | | | | | | | |

## Como preencher

- Tempo, memória e losses: `MyDrive/ccf726/<rodada>/rodada.json`.
- F1 e JSON válido: saída do `python -m evaluation.evaluate ... --nome val/<rodada> --pos-processar` (resumo em `evaluation/results/val/<rodada>/resumo.json`).
- Curva de loss: `MyDrive/ccf726/<rodada>/curva_loss.png` (copie para `training/figuras/` se for usar no artigo).
