# evaluation/

Script único de avaliação, usado para a baseline (Gemini) e para todos os SLMs.

```powershell
python -m evaluation.evaluate --pred-dir data/test/baseline_gemini --nome gemini-2.0-flash
```

A pasta de predições deve ter um `<id>.json` por arquivo do `data/test/manifest.csv`, contendo uma lista de atividades ou `{"atividades": [...]}`. Arquivo ausente ou JSON inválido conta como predição vazia: todas as atividades do gabarito viram FN.

Saídas em `evaluation/results/<nome>/`: `resumo.json`, `por_arquivo.csv` e `erros_formato.json` (quando houver).

## Métricas

| Nível | O que mede | Regra |
|---|---|---|
| 1 — exato | Detecção (P/R/F1 micro) | Casamento por `nome` com `lower().strip()`, guloso um-para-um. É o critério do TCC; dá o mesmo TP/FP/FN que `legacy_tcc/script1.py` (há teste garantindo isso). |
| 1b — aproximado | Detecção tolerante a pequenas diferenças no nome | Nome sem acento e pontuação; similaridade `rapidfuzz.fuzz.ratio` ≥ 0,9; pares de maior similaridade primeiro. |
| 2 | Acurácia por campo nos pares emparelhados | `lugar` (`lugarId` é sinônimo) e texto normalizado; datas comparadas como datetime ISO 8601; `descricao` **sem as tags HTML**, por similaridade ≥ 0,9 (descrição inventada ou omitida = erro); `null` = `""` = ausente. |
| Validade | Formato da saída | % de arquivos com JSON válido; % de atividades válidas no schema (nome obrigatório, datas ISO 8601 com offset). |

Intervalos de confiança de 95% por **bootstrap**: reamostra os 17 arquivos com reposição e recalcula as métricas micro (2000 reamostras, semente 42).

## Diferenças em relação ao script do TCC

- **Nível 1:** idêntico.
- **Nível 2:** pode variar um pouco. O `lugarId` passa a ser comparado (o script antigo ignorava), e a descrição é comparada sem HTML e por similaridade (≥ 0,9) em vez de igualdade exata. As datas não mudam.

## Baseline via API (Gemini)

O Gemini 2.0-Flash do TCC foi descontinuado em 01/06/2026. As saídas originais dele continuam em `data/test/baseline_gemini/` e são avaliadas como `gemini-2.0-flash-tcc`. Para medir eficiência e qualidade nas mesmas condições do SLM, `run_gemini.py` roda um modelo Gemini atual sobre os textos congelados, com o prompt do TCC (`prompts/prompt_tcc.txt`), temperatura 0 e modo JSON:

```powershell
python -m evaluation.run_gemini --modelo gemini-3.6-flash --thinking low
python -m evaluation.evaluate --pred-dir evaluation/predictions/gemini-3.6-flash-low --nome gemini-3.6-flash-low
```

- Predições: `evaluation/predictions/<nome>/<id>.json`.
- Eficiência: `evaluation/results/<nome>/eficiencia.json` e `.csv`, com latência medida no cliente (inclui rede), tokens de entrada, saída e raciocínio, tokens/s e custo estimado pela tabela de preços do script.
- Cada arquivo é chamado `--repeticoes` vezes (padrão 3). A primeira chamada vira a predição; todas entram na latência.

Tabela comparativa:

```powershell
python -m evaluation.compare gemini-2.0-flash-tcc gemini-3.6-flash-low gemini-3.5-flash-lite-minimal -o evaluation/results/BASELINE.md
```
