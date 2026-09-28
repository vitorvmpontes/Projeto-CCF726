# Projeto CCF726 — SLM para Extração de Atividades de Eventos

Projeto da disciplina **CCF726 – Engenharia de Aprendizado de Máquina** (UFV – Campus Florestal).

## Contexto

Este projeto continua o TCC *"Aplicação de Técnicas de Extração de Informação para Automatizar o Cadastro de Atividades no Sistema myMobiConf"*.

No TCC foi construído um pipeline que recebe a programação de um evento (PDF, HTML, planilha ou imagem), extrai o texto e usa o **Google Gemini 2.0-Flash** para convertê-lo em um JSON de atividades (nome, local, datas e descrição). O objetivo era pré-preencher o cadastro no myMobiConf. O pipeline alcançou **F1 de ~89%** na detecção de atividades.

## Objetivo

Substituir o LLM generalista por um **Small Language Model (SLM)** ajustado com fine-tuning para esta tarefa, buscando:

- desempenho comparável ao Gemini;
- menor latência e custo;
- execução local, sem depender de API externa.

A baseline de comparação são os resultados do TCC, avaliados no mesmo conjunto de teste ([dataset-extracao-eventos](https://github.com/vitorvmpontes/dataset-extracao-eventos)).

## Status

Em desenvolvimento. O planejamento e as decisões do projeto estão em `docs/PLANEJAMENTO.md`.

> Os pesos dos modelos (`.gguf`) não são versionados neste repositório.
