# treinamentos/

Uma pasta por rodada de treino (`t1`, `t2`, ...), com tudo o que é preciso para o artigo e para reproduzir:
configuração e log do treino, avaliações (validação e, quando houver, teste) e as predições brutas no teste.

| Rodada | Pasta | Tipo | Teste (F1 exato) |
|---|---|---|---|
| e2b-r1 | `t1/` | **Principal, pré-registrada** | 72,55% |
| e2b-r2 | `t2/` | Exploratória (correções motivadas pelos erros do teste da t1) | — |

Regra: a pasta de uma rodada já avaliada no teste não é alterada. Reavaliações (por exemplo, com outra versão do
pós-processamento) vão para uma subpasta nova com o nome da mudança.
