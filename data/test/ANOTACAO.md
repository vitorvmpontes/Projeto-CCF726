# Regra de anotação do conjunto de teste

Vale para os gabaritos em `ground_truth/` e é o critério usado pelo script de avaliação.

## `nome`

- É **exatamente o nome da atividade**, como aparece no documento.
- Não incluir trechos da descrição: palestrante, tema, subtítulo, horário, local.
- Não acrescentar nada que não esteja no texto.

## `descricao`

- **Determinística:** usa apenas informações presentes no texto da programação, sem inferir nem completar.
- Formatada com tags HTML (`<p>`, `<b>`, `<i>`, `<br>`).
- As tags **não entram na avaliação**: o texto é comparado sem HTML, porque a marcação admite várias formas igualmente corretas.

## `lugar`, `dataInicio`, `dataFim`

- `lugar`: o nome do local exatamente como aparece no texto. Ausente → `null`.
- Datas em ISO 8601 com offset `-03:00`. Ausente → `null`.
- Na avaliação, `null`, `""` e campo ausente são equivalentes.
