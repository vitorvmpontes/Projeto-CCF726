# e2b-r1 reavaliada com o pós-processamento v2 — EXPLORATÓRIO

Mesmas predições de `../predicoes_teste/` (nenhuma inferência nova), avaliadas com `--pp-versao v2` em 2026-11-20.
As regras da v2 foram escritas **depois** de ver os erros do teste da e2b-r1, por isso este número não substitui o
resultado principal (72,55%, pós-processamento v1). Ele mede quanto do erro era só de formato.

| | F1 exato | IC95 | F1 aprox. | início | fim |
|---|---|---|---|---|---|
| e2b-r1 + pp v1 (principal) | 72,55 | [57,65; 84,78] | 81,20 | 40,8 | 39,9 |
| e2b-r1 + pp v2 (exploratório) | 75,87 | [61,11; 87,10] | 81,20 | 45,6 | 42,5 |
| Gemini 2.0-Flash + pp v1 ou v2 | 90,05 | [84,55; 95,13] | 92,50 | 65,0 | 59,2 |

- Travessões no nome normalizados (11 atividades) e faixas de horário separadas (14 datas).
- A recuperação de JSON cortado também foi testada e descartada: no `secom2024-pdf` (único caso) a saída cortada era um
  loop, e recuperá-la derrubava o F1 exato para 73,58 e o aproximado para 79,25.
- O Gemini 2.0 não muda com a v2 (já usava hífen e não colava faixas de horário).
