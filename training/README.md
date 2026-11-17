# training/

Fine-tuning do SLM (Fase 7) no Google Colab gratuito (T4, 16 GB). Modelo base: **Gemma 4 E2B / E4B** com QLoRA 4-bit (Unsloth).

| Arquivo | Para quê |
|---|---|
| `preparar.py` | Converte `data/processed/{train,val}.jsonl` em conversas (`training/dados/`, ignorada pelo git) e monta a validação no formato do teste (`data/val_eval/`) |
| `treino_gemma4.ipynb` | Notebook do Colab: tokens reais, QLoRA, loss só na resposta, melhor checkpoint pelo val, exporta adapter + GGUF para o Drive |
| `EXPERIMENTOS.md` | Tabela das rodadas (uma mudança por vez) |
| `requirements-colab.txt` | Dependências do Colab |

O prompt fica em `inference/prompt.py` e é **o mesmo** no treino e na inferência.

## Ciclo de uma rodada

1. No PC: `python -m training.preparar` (só quando o dataset mudar) e commit/push.
2. No Colab: abrir `training/treino_gemma4.ipynb` (Arquivo → Abrir notebook → GitHub), ajustar a célula 1 e executar tudo. Resultados em `MyDrive/ccf726/<rodada>/`.
3. No PC (RTX 3050): baixar o `.gguf`, subir o `llama-server` e rodar `evaluation.run_slm` + `evaluation.evaluate` na validação rápida (ver o fim do notebook).
4. Registrar em `EXPERIMENTOS.md`.
