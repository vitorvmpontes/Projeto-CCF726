## Qualidade (17 arquivos)

| Experimento | P | R | F1 | IC95 F1 | F1 aprox. | Lugar | Data início | Data fim | Descrição | JSON válido | Schema |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini-2.0-flash-tcc | 89.36 | 90.74 | **90.05** | [84.55, 95.13] | 92.50 | 74.15 | 64.97 | 59.18 | 87.07 | 100.00 | 99.39 |
| gemini-3.6-flash-low | 85.31 | 84.26 | **84.78** | [75.56, 92.68] | 88.51 | 70.33 | 73.26 | 68.50 | 84.62 | 100.00 | 100.00 |
| gemini-3.5-flash-lite-minimal | 79.80 | 73.15 | **76.33** | [62.81, 88.08] | 83.74 | 51.90 | 71.73 | 65.82 | 12.66 | 100.00 | 100.00 |

## Eficiência

| Experimento | Latência mediana (s) | Latência p95 (s) | Tokens/s | Tokens entrada | Tokens saída | Tokens raciocínio | Custo por programação (USD) |
|---|---|---|---|---|---|---|---|
| gemini-3.6-flash-low | 13.79 | 25.93 | 240.4 | 2291 | 3211 | 0 | 0.01376 |
| gemini-3.5-flash-lite-minimal | 6.06 | 15.90 | 390.9 | 2291 | 3093 | 0 | 0.00842 |
