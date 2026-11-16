# Projeto CCF726 — SLM para Extração de Atividades de Eventos

Projeto da disciplina **CCF726 – Engenharia de Aprendizado de Máquina** (UFV – Campus Florestal).

## Contexto

Este projeto continua o TCC *"Aplicação de Técnicas de Extração de Informação para Automatizar o Cadastro de Atividades no Sistema myMobiConf"*.

No TCC foi construído um pipeline que recebe a programação de um evento (PDF, HTML, planilha ou imagem), extrai o texto e usa o **Google Gemini 2.0-Flash** para convertê-lo em um JSON de atividades (nome, local, datas e descrição). O objetivo era pré-preencher o cadastro no myMobiConf. O pipeline alcançou **F1 de 89,4%** na detecção de atividades.

## Objetivo

Substituir o LLM generalista por um **Small Language Model (SLM)** ajustado com fine-tuning para esta tarefa, buscando:

- desempenho comparável ao Gemini;
- menor latência e custo;
- execução local, sem depender de API externa.

A baseline de comparação são os resultados do TCC, avaliados no mesmo conjunto de teste ([dataset-extracao-eventos](https://github.com/vitorvmpontes/dataset-extracao-eventos)).

## Escopo atual

Treinar o SLM com fine-tuning sobre um **dataset sintético** e documentar o processo. O modelo é avaliado no conjunto de teste do TCC, com o Gemini 2.0-Flash (F1 90,05% com o gabarito revisado) como referência. A comparação aprofundada com LLMs (eficiência, custo, vários modelos base) e a integração ao myMobiConf ficam para trabalho futuro.

## Estrutura

| Pasta | Conteúdo |
|---|---|
| `data/` | Conjunto de teste do TCC e dataset de treino/validação (ver `data/README.md`) |
| `extraction/` | Extração de texto (PDF, HTML, planilha, imagem) — fase 1 do pipeline |
| `dataset_builder/` | Geração do dataset sintético (professor Gemini + renderização + filtros) |
| `inference/` | Schema de saída e pós-processamento |
| `evaluation/` | Métricas, avaliação e resultados da baseline |
| `training/` | Fine-tuning no Google Colab |
| `tests/` | Testes (`python -m pytest`) |

## Status

Em desenvolvimento. O planejamento e o registro de decisões estão em `docs/PLANEJAMENTO.md`.

> Os pesos dos modelos (`.gguf`) não são versionados neste repositório.
