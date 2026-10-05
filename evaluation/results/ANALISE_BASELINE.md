# Análise da baseline (Fase 2)

Data: 2026-10-05. Conjunto de teste: 17 arquivos, 324 atividades no gabarito revisado. Os números completos estão em [`BASELINE.md`](BASELINE.md).

## Resumo

| Modelo | F1 exato | F1 aprox. | Latência mediana | Custo por programação |
|---|---|---|---|---|
| Gemini 2.0-Flash (saídas do TCC) | **90,05** [84,55; 95,13] | 92,50 | — | — |
| Gemini 3.6-Flash, thinking `low` | 84,78 [75,56; 92,68] | 88,51 | 13,8 s | US$ 0,0138 |
| Gemini 3.5-Flash-Lite, thinking `minimal` | 76,33 [62,81; 88,08] | 83,74 | 6,1 s | US$ 0,0084 |

O Gemini 2.0-Flash, descontinuado em 01/06/2026, continua sendo a **baseline principal**. Os modelos atuais rodaram com o mesmo prompt e os mesmos textos congelados, mas tiveram desempenho pior. Os intervalos de confiança se sobrepõem, então a diferença entre 2.0-Flash e 3.6-Flash não é conclusiva com 17 arquivos.

## Por que os modelos atuais ficaram abaixo

Contagem de falsos negativos e erros de descrição por categoria:

| Causa | 2.0-Flash | 3.6-Flash | 3.5-Flash-Lite |
|---|---|---|---|
| Nome igual ao gabarito, só que com travessão (`–`) em vez de hífen (`-`) | 0 | 11 | 11 |
| Nome "alongado": título + subtítulo/palestrante, contrariando a regra de anotação | 1 | 17 | 29 |
| Descrição diferente do gabarito (comparação exata) | 57 | 72 | 218 |
| …dos quais: descrição inventada quando o gabarito não tem | 3 | 34 | 139 |

1. **Travessões (todo o ForumCPA):** o texto do PDF usa `–`. Os modelos novos copiam o caractere fielmente, enquanto o gabarito e o 2.0-Flash usam `-`. O casamento aproximado (Nível 1b) já resolve isso.
2. **Convenção de `nome`:** o prompt do TCC só diz "título ou nome oficial". A regra de que o nome não deve incluir subtítulo nem palestrante está no gabarito (`data/test/ANOTACAO.md`), mas não está no prompt. Os modelos novos juntam título e subtítulo (Bioeconomia, OPMED). Também juntam atividades listadas na mesma linha, como "Credenciamento, Coffee Break e Visita aos estandes" no MFP dia 1.
3. **Descrição não determinística:** o 3.5-Flash-Lite inventa descrições genéricas, como "Palestra voltada para o tema…", quando o texto não tem nenhuma. Isso viola a regra de anotação e é corretamente penalizado.

## Eficiência

- O raciocínio foi praticamente desligado: 0 tokens de raciocínio nos dois modelos.
- A saída é bem maior que a entrada (cerca de 3,1 mil tokens de saída para 2,3 mil de entrada), por causa do JSON com HTML. Saída domina custo e latência, o que reforça a decisão da Fase 3 de o modelo gerar só os campos extraídos e o código montar o resto.
- A latência foi medida no cliente e inclui rede. O SLM local será medido na mesma máquina, sem rede.

## Decisões tomadas após a análise (2026-10-05)

- **Gabarito `opmed-html`:** a atividade com `nome` = `"-"` existe assim na programação original e foi mantida. O casamento aproximado passou a tratar nomes formados só por pontuação, que antes eram ignorados; o F1 aproximado do 2.0-Flash foi de 92,19 para 92,50.
- **Prompt da baseline:** mantido o prompt do TCC, sem a regra de `nome`, para a comparação continuar fiel ao artigo. A regra entra no SLM pelos dados de treino.
- **Métrica de descrição:** passou a usar similaridade (`rapidfuzz.fuzz.ratio` ≥ 0,9) sobre o texto sem HTML. Descrição inventada quando o gabarito não tem, ou omitida quando tem, continua contando como erro. Com isso, a acurácia de descrição ficou em 87,07 (2.0-Flash), 84,62 (3.6-Flash) e 12,66 (3.5-Flash-Lite). O Lite continua baixo por inventar descrições.
