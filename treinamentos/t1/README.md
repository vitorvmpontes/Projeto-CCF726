# t1 — e2b-r1 · RESULTADO PRINCIPAL (pré-registrado)

> **Não sobrescrever.** Este é o primeiro resultado do SLM no conjunto de teste, pré-registrado em `docs/PLANEJAMENTO.md`
> (2026-11-19) e executado uma única vez. Ele entra no artigo como o resultado principal. As rodadas seguintes são
> **exploratórias** (motivadas pelos erros deste teste) e são reportadas à parte.

| | |
|---|---|
| Modelo | Gemma 4 E2B (`unsloth/gemma-4-E2B-it`) + QLoRA r16/α16, 2 épocas, lr 2e-4, batch efetivo 8, prompt `v1` |
| Dados | v1.1 (1.348 exemplos de treino; 9 removidos por passarem de 8.192 tokens) |
| Treino | Colab T4, 188 min, pico 11,9 GB, melhor loss de validação 0,0021 |
| Inferência | `llama-server` (llama.cpp, Vulkan) na RTX 3050: base `gemma-4-E2B-it-Q4_K_M.gguf` + LoRA `e2b-r1-lora.F16.gguf`, contexto 16k, temperatura 0, saída livre |
| Pós-processamento | **v1** (o que existia em 2026-11-19) |
| Validação rápida (60) | F1 100% (579/579) |
| **Teste (17)** | **F1 exato 72,55%** [57,65; 84,78] · aprox. 81,20% · bruto 68,99% · Gemini 2.0-Flash 90,05% |

| Arquivo | Conteúdo |
|---|---|
| `rodada.json`, `log_treino.csv`, `curva_loss.png` | Treino (Colab) |
| `val/` | Avaliação na validação rápida |
| `teste/` | Avaliação no teste com pós-processamento v1 (resultado principal) |
| `teste_bruto/` | Avaliação no teste sem pós-processamento |
| `predicoes_teste/` | Saídas brutas do modelo nos 17 arquivos (congeladas) |
| `RESULTADO.md` | Números e análise de erros |
