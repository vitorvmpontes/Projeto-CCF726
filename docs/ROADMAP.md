# Roadmap — Projeto CCF726

Atividades necessárias para o projeto completo, na ordem de execução sugerida. As decisões e justificativas de cada etapa estão em [`PLANEJAMENTO.md`](PLANEJAMENTO.md).

Cada fase termina com um **entregável** que serve de entrada para a fase seguinte.

---

## Fase 0 — Organização do repositório

- [x] Criar o repositório e adicionar o `.gitignore` (pesos fora do git)
- [x] README e documento de planejamento
- [ ] Adicionar o professor (`fabaguiarsilva`) como colaborador no GitHub
- [ ] Criar a estrutura de pastas (`crawler/`, `extraction/`, `dataset_builder/`, `training/`, `evaluation/`, `inference/`, `data/`)
- [ ] Definir o ambiente: `requirements.txt` com versões fixas; notebooks do Colab em `training/`
- [ ] Criar as contas e credenciais necessárias (AWS S3, Hugging Face Hub, API do LLM professor) e guardá-las em `.env`

**Entregável:** repositório estruturado e ambiente reproduzível.

---

## Fase 1 — Revisão da literatura

- [ ] Reaproveitar os trabalhos relacionados do TCC (LMDX, LayoutLM, Neupane et al. etc.)
- [ ] Levantar trabalhos sobre SLMs aplicados à extração de informação e saída estruturada
- [ ] Levantar trabalhos sobre destilação de LLMs e geração de dados sintéticos para fine-tuning
- [ ] Levantar trabalhos sobre LoRA/QLoRA e fine-tuning eficiente
- [ ] Identificar lacunas e justificar a escolha da baseline (Gemini 2.0-Flash do TCC)

**Entregável:** seção de trabalhos relacionados do artigo, em rascunho.

---

## Fase 2 — Conjunto de teste e baseline

Vem antes do dataset de treino: é o "gabarito" do projeto e precisa ficar congelado cedo.

- [ ] Trazer o dataset do TCC (arquivos originais + ground truth) para `data/test/`
- [ ] Fechar a contagem de arquivos (17 × 18) e documentar a decisão
- [ ] Portar o extrator de texto do TCC (fase 1 do pipeline) para `extraction/`
- [ ] Gerar e **congelar** os textos brutos de cada arquivo de teste (`data/test/raw_text/`)
- [ ] Portar o script de avaliação do TCC para `evaluation/`:
  - [ ] Nível 1: detecção (P/R/F1 micro, casamento por nome exato)
  - [ ] Nível 1b: detecção com casamento aproximado
  - [ ] Nível 2: acurácia por campo
  - [ ] Taxa de JSON válido e aderência ao schema
  - [ ] Intervalos de confiança por bootstrap
- [ ] Reexecutar o Gemini sobre os textos congelados e confirmar que os números batem com o TCC (ou registrar a diferença)
- [ ] Instrumentar a medição de eficiência (latência, tokens/s, memória, custo) e medir o Gemini

**Entregável:** script de avaliação único e tabela da baseline reproduzida.

---

## Fase 3 — Schema de saída e pós-processamento

- [ ] Definir o schema de saída do SLM (campos extraídos "como aparecem" no texto)
- [ ] Decidir o tratamento do campo `descricao` (HTML gerado pelo modelo × montado por código)
- [ ] Implementar a normalização de datas/horas para ISO 8601 `-03:00` (inferência de ano, formatos "9h", "09:00", "9h30" etc.)
- [ ] Implementar as regras de ausência (hora de término inferida ou duração padrão)
- [ ] Implementar a montagem do JSON final do myMobiConf (`eventoId`, `tagIds`, `configuracoes`)
- [ ] Validação do objeto final (Pydantic/`jsonschema`)
- [ ] Testes unitários do pós-processamento
- [ ] Adaptar o script de avaliação para avaliar a saída **após** o pós-processamento

**Entregável:** módulo de pós-processamento testado e schema congelado. O dataset de treino depende dele.

---

## Fase 4 — Coleta de dados (crawler)

- [ ] Mapear fontes de programações de eventos (congressos, semanas acadêmicas, SBC, universidades, plataformas de eventos)
- [ ] Implementar o crawler (respeitando `robots.txt` e limites de requisição)
- [ ] Filtrar eventos que coincidam com os do conjunto de teste (anti-vazamento)
- [ ] Armazenar os arquivos brutos no AWS S3 (`fonte/evento/arquivo`)
- [ ] Gerar o manifesto de coleta (URL, data, formato, hash) e remover duplicatas
- [ ] Rodar o extrator da Fase 2 em todos os arquivos coletados → `data/interim/`

**Entregável:** corpus de textos brutos reais no S3, com manifesto.

---

## Fase 5 — Construção do dataset de treino

- [ ] Escolher o LLM professor (testar 2–3 opções em uma pequena amostra e comparar)
- [ ] **Fonte A (destilação):** rotular os textos reais com o LLM professor no schema da Fase 3
- [ ] **Fonte B (sintético):** gerar JSON → texto com ruído, focando nos casos difíceis:
  - [ ] cabeçalhos de seção que não são atividades
  - [ ] atividades com nomes iguais em horários/locais diferentes
  - [ ] títulos quebrados em várias linhas
  - [ ] texto decorativo próximo às atividades
  - [ ] eventos de vários dias e horários de término ausentes
- [ ] Aplicar os filtros automáticos de qualidade (schema, ancoragem do nome no texto, consistência temporal, duplicatas, tamanho em tokens)
- [ ] Revisar manualmente uma amostra e estimar a taxa de erro do professor
- [ ] Dividir em `train`/`val` **por evento**
- [ ] Salvar em JSONL, versionar e escrever o *data card*

**Entregável:** `train.jsonl` e `val.jsonl` versionados e com qualidade documentada.

---

## Fase 6 — Análise exploratória dos dados

- [ ] Distribuição de tokens (entrada + saída), para definir o `max_seq_length`
- [ ] Atividades por evento, formatos de origem, proporção real × sintético
- [ ] Frequência dos casos difíceis em treino, validação e teste
- [ ] Gráficos para o artigo

**Entregável:** notebook de EDA e figuras.

---

## Fase 7 — Triagem dos modelos candidatos

- [ ] Confirmar as versões mais recentes de cada família no Unsloth (Qwen, Gemma, Llama, Phi)
- [ ] Definir o prompt curto único (papel + ano de referência + texto)
- [ ] Rodar todos os candidatos em zero/few-shot no `val`, com decodificação gulosa
- [ ] Medir qualidade e eficiência com o script da Fase 2
- [ ] Escolher 2–3 finalistas para o fine-tuning

**Entregável:** tabela de triagem e modelos finalistas escolhidos.

---

## Fase 8 — Fine-tuning

- [ ] Notebook de treino no Colab com QLoRA + Unsloth:
  - [ ] chat template nativo do modelo, idêntico em treino e inferência
  - [ ] loss só na resposta (`train_on_responses_only`)
  - [ ] JSON serializado com `ensure_ascii=False`
  - [ ] `eval_dataset` e seleção do melhor checkpoint
  - [ ] seeds fixas e logs de treino salvos
- [ ] Treinar os finalistas com a mesma configuração-base
- [ ] Busca de hiperparâmetros (rank, learning rate, épocas) nos finalistas, avaliada no `val`
- [ ] Escolher a configuração final de cada finalista
- [ ] Exportar para GGUF (Q4_K_M e Q8_0)
- [ ] Publicar adapter + GGUF no Hugging Face Hub, com model card

**Entregável:** modelos ajustados, persistidos e versionados.

---

## Fase 9 — Avaliação final

- [ ] Rodar os modelos finais no conjunto de teste (**uma única vez**)
- [ ] Tabela principal: Gemini × SLMs (zero-shot e fine-tuned) × métricas de qualidade e eficiência
- [ ] Resultados por arquivo, comparáveis às Tabelas 1 e 2 do TCC
- [ ] Ablações:
  - [ ] zero-shot × fine-tuned
  - [ ] tamanho do modelo
  - [ ] quantização Q4 × Q8
  - [ ] com × sem dados sintéticos (fonte B)
- [ ] Análise de erros qualitativa por categoria
- [ ] Responder às perguntas de pesquisa (QP1–QP4)

**Entregável:** resultados finais, tabelas e análise de erros.

---

## Fase 10 — Produção e integração

- [ ] `ModelFile` do Ollama com o template e os parâmetros do modelo final
- [ ] Reescrever o serviço de inferência:
  - [ ] cada chamada independente (sem reaproveitar `context`)
  - [ ] `num_ctx` adequado
  - [ ] saída restrita por JSON Schema
  - [ ] pós-processamento da Fase 3
- [ ] Expor uma API (por exemplo FastAPI) com o mesmo contrato usado hoje pelo backend
- [ ] Integrar ao backend NestJS do myMobiConf, substituindo a chamada ao Gemini
- [ ] Teste ponta a ponta: upload → extração → revisão na interface
- [ ] Documentar como subir o serviço (README)

**Entregável:** SLM em produção no myMobiConf.

---

## Fase 11 — Artigo e apresentação

- [ ] Estrutura do artigo (≤ 8 páginas): introdução, trabalhos relacionados, metodologia (dados, modelos, treino, avaliação), resultados, discussão, conclusão
- [ ] Figuras: pipeline atualizado, EDA, tabelas de resultados
- [ ] Discutir as limitações (layout espacial continua sem solução; qualidade do professor; tamanho do teste)
- [ ] Revisar e finalizar o README do repositório com instruções de reprodução
- [ ] Apresentação de 10 minutos

**Entregável:** artigo final, apresentação e repositório reprodutível.

---

## Dependências entre fases

```
Fase 0 → Fase 2 → Fase 3 ─┐
               └→ Fase 4 ─┴→ Fase 5 → 6 → 7 → 8 → 9 → 10 → 11
Fase 1 (em paralelo) ──────────────────────────────────────→ 11
```

- A Fase 1 pode correr em paralelo com as demais.
- A Fase 4 (crawler) pode começar junto com a Fase 3, mas o dataset (Fase 5) depende das duas.
- A Fase 7 pode começar com o `val` parcial, assim que houver algumas centenas de exemplos.
