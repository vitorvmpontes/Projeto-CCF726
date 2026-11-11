# inference/

Contratos de dados e pós-processamento da extração. O serviço do SLM (Ollama + API) entra aqui na Fase 10.

| Arquivo | Conteúdo |
|---|---|
| `schema.py` | `AtividadeExtraida`: o que o modelo devolve, e também o formato dos rótulos de treino e do gabarito. `AtividadeMyMobiConf`: o objeto final. `json_schema_saida()`: JSON Schema para geração restrita. |
| `postprocess.py` | `pos_processar(resposta_bruta, texto_entrada)` valida e corrige a saída do modelo. `para_mymobiconf(...)` monta o objeto final com os campos fixos. |

## Saída do modelo (schema congelado na Fase 3)

```json
{"atividades": [
  {"nome": "Workshop de Docker",
   "lugar": "Sala 2",
   "dataInicio": "2025-09-10T14:00:00-03:00",
   "dataFim": null,
   "descricao": "<p><b>Palestrante:</b> <b>Mariana Silva</b></p>"}
]}
```

## O que o pós-processamento faz (sem inventar informação)

- **Parse tolerante:** aceita ```` ```json ````, `<think>` e texto em volta do JSON.
- **Datas:**
  - ISO 8601 com segundos e offset `-03:00`;
  - repara anos malformados (`2S024`);
  - corrige o ano pelo texto quando ele cita anos;
  - data sem hora ou inválida → `null`;
  - fim antes do início → `null`.
- **`descricao`:** HTML sanitizado; só `<p>`, `<b>`, `<i>`, `<br>`, `<hr>`, sem atributos.
- **Nome e local:** espaços normalizados; atividade sem nome é descartada.
- **Repetições:** só corta repetições idênticas seguidas além de 2 (modelo em loop); duplicatas legítimas ficam.
- **Correções:** todas são contadas em `Resultado.correcoes`.

```python
from inference.postprocess import pos_processar, para_mymobiconf

res = pos_processar(resposta_do_modelo, texto_da_programacao)
final = para_mymobiconf(res.atividades, evento_id="...")
```
