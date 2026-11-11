# Planejamento e Registro de Decisões — Projeto CCF726

**SLM para extração de atividades de programações de eventos (continuação do TCC myMobiConf)**

- Disciplina: CCF726 — Engenharia de Aprendizado de Máquina (UFV-CAF) — Prof. Fabrício A. Silva
- Aluno: Vitor Vasconcelos de M. Pontes
- Entregas: parciais em 30/09/2026 e 09/11/2026 · final e apresentação em 02/12/2026
- Repositório: https://github.com/vitorvmpontes/Projeto-CCF726

> Documento vivo. Cada decisão tem um status: **Decidido**, **Proposto** (a validar) ou **Em aberto**.
> Quando uma decisão mudar, registre a data e o motivo na seção 12 em vez de apagar o histórico.

---

## 1. Contexto e objetivo

No TCC, foi construído um pipeline de duas fases para automatizar o cadastro de atividades no myMobiConf:

1. **Extração de texto**: roteador por tipo de arquivo — PyMuPDF (PDF), BeautifulSoup (HTML), Pandas (XLS), Google Vision OCR (imagens). A saída é sempre uma string de texto bruto.
2. **Extração semântica**: Google Gemini 2.0-Flash com engenharia de prompt (role prompting, schema explícito, one-shot, regras de negócio, temperatura 0, modo JSON nativo).

A seção de trabalhos futuros do TCC propõe substituir o LLM generalista por um **Small Language Model (SLM) ajustado com fine-tuning** para a tarefa, visando:

- menor latência e custo operacional;
- execução local, sem dependência de API externa nem envio de dados a terceiros;
- desempenho comparável ao Gemini na tarefa específica.

**Objetivo deste projeto:** treinar, avaliar e colocar em produção um SLM que substitua o Gemini **apenas na fase 2** do pipeline, comparando-o com a baseline do TCC.

**Fora do escopo** (trabalho futuro 2 do TCC): tratar layout espacial (VLMs ou bounding boxes). Essa limitação continua existindo, porque o SLM recebe o mesmo texto linearizado. Isso deve ficar explícito no artigo.

---

## 2. Perguntas de pesquisa

- **QP1.** Um SLM ajustado com fine-tuning atinge desempenho de detecção (F1) comparável ao Gemini 2.0-Flash no mesmo conjunto de teste?
- **QP2.** Qual modelo base (família e tamanho) rende o melhor resultado nesta tarefa, em português?
- **QP3.** Quanto o fine-tuning melhora em relação ao mesmo modelo usado em zero/few-shot?
- **QP4.** Qual o ganho em eficiência (latência, throughput, memória, custo) do SLM local em relação à API?

---

## 3. Baseline

| Item | Valor |
|---|---|
| Modelo | Google Gemini 2.0-Flash (API, modo JSON, temperatura 0) |
| Conjunto de teste | 10 eventos, 18 arquivos (HTML, PDF, XLS, imagem), 324 atividades |
| Ground truth | https://github.com/vitorvmpontes/dataset-extracao-eventos |
| Detecção (micro) | Precisão 88,75% · Revocação 90,12% · **F1 89,43%** |
| Acurácia por campo | Tabela 2 do TCC (por arquivo) |

**Decisões sobre a baseline**

- **Decidido**: o dataset do TCC é usado **exclusivamente como conjunto de teste**. Ele nunca entra no treino nem na validação/seleção de hiperparâmetros, para evitar vazamento de dados.
- **Proposto**: reexecutar o Gemini com o **mesmo script de avaliação** usado nos SLMs, para que as duas linhas da tabela final saiam do mesmo código. **Atualização (2026-09-29):** as saídas originais do Gemini 2.0-Flash já estão salvas em `data/test/baseline_gemini/`, e o script original reproduz o F1 de 0,8943. Não é preciso reexecutar a API.
- **Proposto**: congelar os **textos brutos** gerados pela fase 1 para cada arquivo de teste (`data/test/raw_text/`). Todos os modelos (Gemini e SLMs) recebem exatamente as mesmas strings, e a única variável do experimento passa a ser o modelo.
- **Resolvido**: são 18 arquivos, dos quais 17 são avaliados (`secom2023-img` não tem ground truth).

---

## 4. Dataset

### 4.1 Fontes

O treino precisa de exemplos (texto bruto → JSON de atividades) em volume muito maior que os 324 do teste. Serão combinadas duas fontes:

| Fonte | Como | Prós | Contras |
|---|---|---|---|
| **A. Real + rótulo por LLM professor (destilação)** | Crawler coleta programações reais (sites de congressos, semanas acadêmicas, SBC, universidades, plataformas de eventos). O texto é extraído com o próprio pipeline da fase 1, e um LLM grande gera o JSON. | Ruído realista (quebras de linha, OCR, cabeçalhos). Atende ao item 3.1 da especificação (crawler + armazenamento). | O aluno herda os erros do professor, então os rótulos precisam de filtros e revisão. |
| **B. 100% sintético** | O LLM gera primeiro o JSON (a "verdade") e depois uma programação textual correspondente, com ruído injetado de propósito. | Rótulo correto por construção. Permite gerar sob demanda os casos difíceis que o TCC encontrou. | Texto pode sair "limpo demais" e com distribuição diferente da real. |

- **Decidido**: usar dataset sintético gerado por LLM.
- **Proposto**: usar A como fonte principal e B como aumento de dados focado em casos difíceis:
  - cabeçalhos de seção que **não** são atividades (SECOM2023);
  - atividades com o mesmo nome em horários/locais diferentes (SEBRAE);
  - títulos longos quebrados em várias linhas (WIT2025);
  - texto decorativo próximo a atividades (MFP2025);
  - eventos de vários dias, horário de término ausente, formatos de hora variados ("9h", "09:00", "9h30").
- **Em aberto**: qual LLM professor usar (Gemini, GPT, Claude ou um modelo aberto grande). Critérios: qualidade, custo e termos de uso para gerar dados de treino.
- **Em aberto**: tamanho-alvo. Referência inicial: 1.500–3.000 exemplos de treino, ajustável conforme a curva de aprendizado na validação.

### 4.2 Controle de qualidade dos rótulos

Filtros automáticos aplicados a todo exemplo gerado:

1. JSON válido e aderente ao schema (validação com Pydantic ou `jsonschema`).
2. **Ancoragem**: todo `nome` aparece literalmente, ou quase (similaridade ≥ limiar), no texto de entrada. Isso evita atividades alucinadas.
3. Consistência temporal: `fim ≥ inicio`, datas dentro do período do evento.
4. Sem atividades duplicadas (mesmo nome + mesmo horário).
5. Tamanho em tokens (entrada + saída) ≤ contexto de treino. Exemplos maiores são divididos por dia/bloco, não truncados.

Além disso, **revisão manual de uma amostra** (por exemplo 5% ou 50 exemplos) para estimar a taxa de erro do professor. Esse número entra no artigo.

### 4.3 Divisão (splits)

| Split | Origem | Uso |
|---|---|---|
| `train` | Fontes A + B | Fine-tuning |
| `val` | Fonte A (majoritariamente real) | Seleção de modelo, hiperparâmetros, early stopping |
| `test` | **Dataset do TCC (intocado)** | Avaliação final e comparação com a baseline |

- **Proposto**: a divisão train/val é feita **por evento**, e não por atividade. Atividades do mesmo evento nunca ficam em splits diferentes.
- **Proposto**: remover do crawler qualquer evento que coincida com os 10 do teste (SECOM, WIT, SEBRAE etc.), inclusive de outros anos, se o layout for o mesmo.

### 4.4 Armazenamento e organização

- **Proposto**: dados brutos coletados (HTML/PDF/imagens) no **AWS S3**, conforme a especificação, organizados por `fonte/evento/arquivo`. Metadados de coleta (URL, data, formato, hash) em um manifesto.
- Datasets processados em **JSONL** (um exemplo por linha), versionados e com um *data card* no repositório (ou no Hugging Face Datasets).
- Estrutura prevista:

```
data/
  raw/            # (S3, ignorado no git) arquivos originais coletados
  interim/        # (ignorado no git) textos extraídos pela fase 1
  processed/
    train.jsonl
    val.jsonl
  test/
    raw_text/     # textos brutos congelados do dataset do TCC
    ground_truth/ # JSONs anotados do TCC
  manifest.csv
```

Formato de cada linha JSONL:

```json
{"id": "...", "evento": "...", "fonte": "real|sintetico", "formato_origem": "pdf|html|xls|img",
 "ano_referencia": 2025, "texto": "...", "atividades": [ ... ]}
```

---

## 5. Schema de saída e pós-processamento

**Decidido (2026-10-21)** — revisa a proposta de 2026-09-28, que previa datas "como aparecem" montadas pelo código.

O **SLM gera** os mesmos 5 campos do gabarito (`inference/schema.py`, classe `AtividadeExtraida`):

```json
{"atividades": [
  {"nome": "...", "lugar": "... ou null", "dataInicio": "2025-09-10T09:00:00-03:00", "dataFim": "... ou null", "descricao": "<p>... <b>Nome</b></p>"}
]}
```

- **Datas:** o modelo já gera ISO 8601 com offset `-03:00`. O ano é inferido do texto.
- **Descrição:** o modelo já gera o HTML (`<p>`, `<b>`, `<i>`, `<br>`). A avaliação ignora as tags.
- **Hora de fim ausente:** fica `null` (não é inferida).
- **Rótulos de treino:** são exatamente o formato do gabarito, sem conversão.

O **código** (`inference/postprocess.py`) não inventa informação. Ele valida e corrige formato:

1. Parse tolerante: cercas ```` ```json ````, `<think>`, texto antes ou depois do JSON.
2. Datas:
   - completa segundos e offset, força `-03:00`;
   - repara anos malformados (`2S024` → `2024`);
   - se o texto cita anos e o ano da data não está entre eles, usa o ano mais citado;
   - data sem hora ou inexistente → `null`;
   - `dataFim` anterior a `dataInicio` → `null`.
3. HTML sanitizado: só tags permitidas, sem atributos, tags fechadas.
4. Nome e local com espaços normalizados; atividade sem nome é descartada.
5. Repetições idênticas seguidas além de 2 são cortadas (sinal de loop). Duplicatas legítimas, como no SEBRAE, são mantidas.
6. `para_mymobiconf` injeta `eventoId`, `tagIds` e `configuracoes`, mapeia `lugar` → `lugarId` e valida com Pydantic.

Todas as correções são contadas e aparecem no resultado da avaliação (`--pos-processar`).

Tradeoffs aceitos:

- O modelo gera mais tokens que no schema compacto (cerca de 2× nos gabaritos) e pode errar formato. O pós-processamento cobre os erros de formato, mas não os de conteúdo.
- Em textos sem ano (6 de 18), o ano depende do modelo.

Validações:

- Aplicado aos 17 gabaritos, o pós-processamento não altera nenhum campo (teste automático).
- Nas baselines, a detecção não muda. No Gemini 2.0-Flash, ele reparou 2 anos malformados (`dataInicio` 64,97 → 65,31).

**Proposto**: usar geração restrita por JSON Schema na inferência (`json_schema_saida()` → `format` do Ollama ou gramática do llama.cpp) para garantir JSON válido.

---

## 6. Modelos candidatos

### 6.1 Critérios de seleção

1. **Português**: a tarefa é em PT-BR, e famílias com treino multilíngue forte tendem a ir melhor.
2. **Janela de contexto real ≥ 8k tokens**: programações longas mais o JSON de saída passam facilmente de 4k.
3. **Licença** que permita fine-tuning e uso.
4. **Suporte no Unsloth** (treino no Colab) e **no llama.cpp/Ollama** (inferência e GGUF).
5. Faixa de tamanho de ~3B a ~12B. O tamanho não é restrição forte, porque a máquina de produção tem folga, mas a eficiência é uma das perguntas de pesquisa.

### 6.2 Lista inicial (Proposto, confirmar as versões mais recentes no Unsloth antes de começar)

| Candidato | Tamanho | Por quê |
|---|---|---|
| Qwen3 (ou versão mais recente) | 4B e 8B | Forte em multilíngue e em saída estruturada/JSON; contexto longo; amplo suporte no Unsloth. Permite comparar dois tamanhos da mesma família. |
| Gemma 3 | 4B e 12B | Multilíngue forte; contexto longo (128k); bom desempenho por parâmetro. |
| Llama 3.1 / 3.2 | 8B / 3B | Referência amplamente usada na literatura de fine-tuning; facilita comparação com outros trabalhos. |
| Phi-4-mini | 3,8B | Sucessor do Phi-3 usado no `saulin_v1`; bom em raciocínio para o tamanho. Serve de controle para medir o ganho de trocar de família. |

**Descartado**: Phi-3-mini-4k, por causa do contexto de 4k e do português mais fraco.

### 6.3 Protocolo de seleção

1. **Triagem zero/few-shot**: todos os candidatos, com o mesmo prompt curto, no `val`. Métricas da seção 8.
2. **Fine-tuning** dos 2–3 melhores da triagem, com o mesmo dataset e a mesma configuração-base.
3. **Busca de hiperparâmetros** (seção 7) apenas nos finalistas.
4. **Avaliação final no `test`**: somente os modelos escolhidos, **uma única vez**.

Isso responde QP2 e QP3 e gera a tabela principal do artigo: modelo × (zero-shot, fine-tuned) × métricas.

---

## 7. Treinamento

**Proposto** (ajustes em relação ao notebook-base usado no `saulin_v1`):

| Aspecto | Decisão |
|---|---|
| Método | QLoRA (4-bit) com Unsloth + TRL `SFTTrainer` |
| Formato do prompt | **Chat template nativo do modelo base**, idêntico em treino, validação e inferência (inclusive no `ModelFile` do Ollama) |
| Prompt de instrução | Curto e fixo (papel + ano de referência + texto). O schema é internalizado pelo fine-tuning, e o prompt longo do Gemini não é necessário |
| Loss | Apenas sobre a resposta (`train_on_responses_only`), não sobre o texto de entrada |
| Serialização do JSON | `ensure_ascii=False` (acentos literais, sem `ç`) |
| `max_seq_length` | Definido a partir da distribuição real de tokens do dataset (p95/p99), nunca truncando exemplos |
| Validação | `eval_dataset` = `val`, avaliação por época/steps, escolha do melhor checkpoint |
| Decodificação na avaliação | Gulosa (temperatura 0) |
| Reprodutibilidade | Seed fixa, versões das bibliotecas fixadas, log de treino salvo (CSV ou W&B) |

**Busca de hiperparâmetros** (grade pequena, custo do Colab em mente):

- LoRA rank `r` ∈ {16, 32, 64}, com `alpha = 2r`
- learning rate ∈ {1e-4, 2e-4}
- épocas ∈ {1, 2, 3}, com early stopping pela loss/métrica de validação

**Persistência** (item 3.3 da especificação):

- Adapter LoRA e GGUF quantizado (Q4_K_M e, para ablação, Q8_0) publicados no **Hugging Face Hub**, com model card. Os pesos não vão para o GitHub.
- O repositório guarda apenas o `ModelFile` e a referência (repo/revisão) do modelo no Hub.

---

## 8. Avaliação

### 8.1 Métricas de qualidade (compatíveis com o TCC)

- **Nível 1, detecção de atividades**: precisão, revocação e F1 **micro**, casando atividades pelo `nome` exato (critério do TCC). Reportar por arquivo e global.
- **Nível 1b, detecção com casamento aproximado** (complementar): casamento por similaridade de string (por exemplo ≥ 0,9) com emparelhamento um-para-um. Mede o efeito dos títulos truncados sem penalizar duas vezes.
- **Nível 2, acurácia por campo**: lugar, data/hora de início, data/hora de fim e descrição, nas atividades detectadas. As datas são comparadas **após** a normalização, para comparar com o TCC.
- **Taxa de JSON válido** e **taxa de aderência ao schema**, antes de qualquer correção.

### 8.2 Métricas de eficiência (novas)

- Latência por programação (média e p95) e tempo até o primeiro token.
- Throughput (tokens/s de geração).
- Pico de memória (VRAM/RAM).
- Custo por programação: tokens × preço para o Gemini; custo estimado de hardware/energia para o SLM local.
- Todas medidas no **mesmo hardware** para os SLMs, com o hardware descrito no artigo.

### 8.3 Protocolo

- Mesmos textos brutos congelados para todos os modelos (seção 3).
- Mesmo script de avaliação para todos, incluindo o Gemini.
- O conjunto de teste é pequeno (≈17–18 arquivos), então reportar intervalos de confiança por **bootstrap** sobre arquivos junto do F1 micro.
- Análise de erros qualitativa, por categoria (cabeçalho como atividade, nome truncado, horário trocado, local alucinado), comparável à discussão do TCC.

### 8.4 Ablações planejadas

- Zero-shot × fine-tuned (mesmo modelo base).
- Tamanho do modelo (4B × 8B/12B na mesma família).
- Quantização Q4_K_M × Q8_0 (qualidade × eficiência).
- Com × sem dados sintéticos da fonte B (os casos difíceis ajudam?).

---

## 9. Produção / integração

- **Proposto**: servir o modelo via **Ollama** na máquina local, com uma API (FastAPI) que recebe o texto bruto e devolve o JSON final (após o pós-processamento). Ela substitui a chamada ao Gemini no backend NestJS do myMobiConf.
- Correções necessárias no `main.py` atual:
  - não reaproveitar `context` entre chamadas (cada programação é independente);
  - `num_ctx` compatível com o tamanho real das entradas (o atual `4068` é insuficiente);
  - remover o tratamento de `<think>` (decisão da seção 5);
  - usar o mesmo template e prompt curto do treino.

---

## 10. Estrutura prevista do repositório

```
Projeto-CCF726/
  README.md
  docs/                 # planejamento, artigo, apresentação
  data/                 # ver seção 4.4 (brutos no S3)
  crawler/              # coleta de programações
  extraction/           # fase 1 (roteador de extratores, reaproveitado do TCC)
  dataset_builder/      # rotulagem pelo professor, geração sintética, filtros, splits
  training/             # notebooks/scripts de fine-tuning (Colab)
  evaluation/           # script de avaliação, métricas, relatórios
  inference/            # ModelFile, pós-processamento, API
  models/               # (ignorado no git) GGUF local
```

---

## 11. Mapeamento com a especificação da disciplina

| Etapa da especificação | Como é atendida |
|---|---|
| 1. Definição do problema e dados | Continuação do TCC; dados vêm do crawler + LLM professor; teste = dataset do TCC |
| 2. Revisão da literatura + baseline | Trabalhos do TCC + literatura de SLMs, destilação e fine-tuning para extração de informação; baseline = Gemini 2.0-Flash (TCC) |
| 3.1 Coleta (crawler/API + armazenamento) | Crawler de programações; brutos no AWS S3 |
| 3.2 Preparação, limpeza, visualização, atributos | Extração de texto, rotulagem, filtros de qualidade, análise exploratória (tokens, atividades por evento, formatos), splits |
| 3.3 Criação do modelo e hiperparâmetros | Triagem de candidatos, QLoRA, busca de hiperparâmetros, persistência no HF Hub |
| 3.4 Validação e comparação com a baseline | Seção 8 |
| 4. Artigo (≤ 8 páginas) + apresentação de 10 min | 02/12/2026 |

---

## 12. Registro de decisões

| Data | Decisão | Status | Motivo |
|---|---|---|---|
| 2026-09-28 | Dataset do TCC usado apenas como teste | Decidido | Evitar vazamento e manter comparação justa com a baseline |
| 2026-09-28 | Baseline = métricas do Gemini 2.0-Flash no TCC | Decidido | Continuidade direta do trabalho |
| 2026-09-28 | Treino com dataset sintético/destilado gerado por LLM | Decidido | Volume de dados necessário para fine-tuning |
| 2026-09-28 | Sem `<think>`; datas por pós-processamento determinístico | Decidido | Menos tokens e latência; regras testáveis; compatível com geração restrita a JSON |
| 2026-09-28 | Adicionar métricas de eficiência | Decidido | Principal argumento do SLM (QP4) |
| 2026-09-28 | Comparar vários modelos base antes de escolher | Decidido | QP2; tamanho não é restrição forte |
| 2026-09-28 | Pesos fora do GitHub (`.gitignore` + HF Hub) | Decidido | Limite de 100 MB por arquivo no GitHub |
| 2026-09-28 | Modelos `saulin_v1`/`saulin_v2` foram só um teste e não servem de referência | Decidido | Novas versões do saulin serão treinadas do zero |
| 2026-09-29 | Ground truth e baseline vêm do repositório de trabalho do TCC (`POC---Vitor-`), não do repositório público | Decidido | É a versão que reproduz os números do artigo (F1 0,8943) |
| 2026-09-29 | Baseline = saídas do Gemini 2.0-Flash (temperatura 0, modo JSON) já salvas | Decidido | Foi o que rodou no TCC; não depende de reexecutar a API |
| 2026-09-29 | OCR com Google Vision `TEXT_DETECTION` | Decidido | Mesmo modo usado para gerar os textos do teste |
| 2026-09-29 | Revisar todos os gabaritos com uma regra de anotação única | Concluído (2026-10-05) | Nomes revisados e confirmados; regra em `data/test/ANOTACAO.md` |
| 2026-10-05 | `nome` = exatamente o nome da atividade, sem trechos da descrição | Decidido | Regra de anotação |
| 2026-10-05 | `descricao` determinística (só informações do texto), em HTML; tags não entram na avaliação | Decidido | A marcação HTML admite várias formas corretas |
| 2026-10-05 | OCR via Google Vision REST com chave de API (`GOOGLE_VISION_API_KEY`) | Decidido | Mesmo método do TCC; dispensa service account e a lib `google-cloud-vision` |
| 2026-10-05 | HTML: uma linha por elemento de bloco; planilha: uma linha por linha, células separadas por ` \| ` | Decidido | O TCC não registrou o formato; esta forma preserva a estrutura |
| 2026-10-05 | Nível 1b: `rapidfuzz.fuzz.ratio` ≥ 0,9 sobre nomes sem acento e pontuação | Decidido | Tolera diferenças pequenas sem aceitar nomes truncados |
| 2026-10-05 | IC 95% por bootstrap sobre arquivos (2000 reamostras, semente 42) | Decidido | Conjunto de teste pequeno (17 arquivos) |
| 2026-10-05 | Baseline principal = saídas salvas do Gemini 2.0-Flash (F1 90,05% com gabarito revisado) | Decidido | Modelo descontinuado em 01/06/2026; as saídas do TCC seguem válidas |
| 2026-10-05 | Baseline via API atual: `gemini-3.6-flash` (thinking `low`) e `gemini-3.5-flash-lite` (thinking `minimal`) | Decidido | 3.6-flash é o substituto oficial indicado pelo Google; 3.5-flash-lite é o mais próximo do 2.0-Flash em custo e sem raciocínio |
| 2026-10-05 | Prompt da baseline mantido igual ao do TCC (sem a regra de `nome`) | Decidido | Comparação fiel ao artigo; a regra entra no SLM pelos dados de treino |
| 2026-10-05 | `descricao` comparada por similaridade ≥ 0,9 (sem HTML); inventada ou omitida = erro | Decidido | Igualdade exata punia diferenças de pontuação final |
| 2026-10-05 | Atividade com `nome` = "-" no `opmed-html` mantida | Decidido | Existe assim na programação original |
| 2026-10-05 | Fase 2 concluída | Concluído | Baseline em `evaluation/results/BASELINE.md` e análise em `ANALISE_BASELINE.md` |
| 2026-10-21 | SLM gera datas em ISO 8601 completo (revisa a decisão de 2026-09-28) | Decidido | Rótulos iguais ao gabarito; pós-processamento valida e repara |
| 2026-10-21 | Ano inferido do texto (pelo modelo; o código corrige quando o texto cita anos) | Decidido | Não depende de dados externos ao texto |
| 2026-10-21 | SLM gera a `descricao` em HTML; código só sanitiza | Decidido | Mantém o formato do myMobiConf e do gabarito |
| 2026-10-21 | `dataFim` ausente fica `null` | Decidido | Regra "só informação do texto"; organizador completa na revisão |
| 2026-10-21 | Campos fixos (`eventoId`, `tagIds`, `configuracoes`) montados pelo código | Decidido | Não gastar tokens nem dar margem a erro |
| 2026-10-21 | Fase 3 concluída: schema congelado (`inference/schema.py`) | Concluído | Pós-processamento testado (`tests/test_postprocess.py`) |
| 2026-10-21 | Fase 5 começa pela fonte B (sintética); a fonte A entra depois da Fase 4 | Decidido | Não bloquear triagem e fine-tuning esperando o crawler |
| 2026-10-21 | Fonte B: LLM gera o JSON do evento, código renderiza o texto (4 layouts × ruídos) | Decidido | Rótulo correto por construção; controle dos casos difíceis |
| 2026-10-21 | Professor: `gemini-3.8-flash` | Decidido | Flash mais recente; custo baixo; regras de anotação no prompt + filtros |
| 2026-10-21 | v1 com ~1.000 exemplos (500 eventos × 2 textos) | Decidido | Crescer só se a curva de aprendizado na validação pedir |
| 2026-10-21 | O ano sempre aparece no texto sintético | Decidido | O rótulo precisa ser inferível do texto (decisão de inferir o ano do texto) |
| 2026-10-21 | Não gerar grades com horários separados dos nomes | Decidido | Associação horário→atividade impossível pelo texto; ensinaria a alucinar |

---

## 13. Tarefas (roadmap)

### Até a 2ª entrega parcial (09/11/2026)

- [ ] Revisão da literatura: SLMs para extração de informação, destilação de LLMs, fine-tuning com LoRA/QLoRA
- [ ] Fechar a contagem de arquivos do teste (17 × 18) e congelar os textos brutos do teste
- [ ] Portar o script de avaliação do TCC para `evaluation/` e reproduzir os números da baseline
- [ ] Definir o schema final de saída do SLM e implementar o pós-processamento de datas, com testes
- [ ] Implementar o crawler e o armazenamento no S3
- [ ] Escolher o LLM professor e gerar o dataset (fontes A e B) com os filtros de qualidade
- [ ] Análise exploratória do dataset (distribuição de tokens, formatos, atividades por evento)
- [ ] Triagem zero/few-shot dos candidatos no `val`

### Até a entrega final (02/12/2026)

- [ ] Fine-tuning dos finalistas e busca de hiperparâmetros
- [ ] Avaliação final no teste (qualidade + eficiência), bootstrap e ablações
- [ ] Análise de erros qualitativa
- [ ] Publicar modelos no Hugging Face Hub; atualizar o `ModelFile` e a API de inferência
- [ ] Integração com o myMobiConf (substituir a chamada ao Gemini)
- [ ] Artigo (≤ 8 páginas) e apresentação (10 min)

---

## 14. Questões em aberto

1. Qual LLM professor usar para rotular/gerar os dados?
2. `descricao` em HTML gerado pelo modelo ou montado por código?
3. Tamanho-alvo do dataset de treino.
4. Hardware exato de produção (para medir eficiência e definir a quantização).
5. Regra de anotação dos gabaritos (o que conta como `nome` da atividade).
