"""Roda um modelo Gemini sobre os textos congelados do conjunto de teste.

Usado para medir a baseline via API nas mesmas condições do SLM: mesmos
textos de entrada (data/test/raw_text/), mesmo prompt do TCC
(evaluation/prompts/prompt_tcc.txt), temperatura 0 e saída em modo JSON.

Para cada arquivo avaliado do manifest:
- salva a predição em evaluation/predictions/<nome>/<id>.json
  (se a resposta não for JSON válido, salva o texto bruto mesmo, e o
  avaliador conta como JSON inválido);
- mede latência, tokens de entrada/saída/raciocínio e custo estimado.

Ao final grava evaluation/results/<nome>/eficiencia.json e eficiencia.csv.
A qualidade é medida depois com:
    python -m evaluation.evaluate --pred-dir evaluation/predictions/<nome> --nome <nome>

Uso (na raiz do repositório, com GEMINI_API_KEY no .env):
    python -m evaluation.run_gemini --modelo gemini-3.6-flash --thinking low
    python -m evaluation.run_gemini --modelo gemini-3.5-flash-lite --thinking minimal
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv

# Preço em USD por 1M de tokens (tier pago, texto), consultado em 2026-10-05 em
# https://ai.google.dev/gemini-api/docs/pricing. O raciocínio ("thinking") é
# cobrado como saída. O gemini-2.0-flash fica só como referência histórica.
PRECOS_USD_POR_1M = {
    "gemini-3.6-flash": {"entrada": 0.75, "saida": 3.75},  # até 31/12/2026
    "gemini-3.7-flash": {"entrada": 0.75, "saida": 3.75},
    "gemini-3.8-flash": {"entrada": 0.75, "saida": 3.75},
    "gemini-3.5-flash": {"entrada": 1.50, "saida": 9.00},
    "gemini-3.5-flash-lite": {"entrada": 0.30, "saida": 2.50},
    "gemini-3.1-flash-lite": {"entrada": 0.25, "saida": 1.50},
    "gemini-2.0-flash": {"entrada": 0.10, "saida": 0.40},
}

TEST_DIR = Path("data/test")
PROMPT = Path("evaluation/prompts/prompt_tcc.txt")
RETRY_CODES = {429, 500, 502, 503, 504}


def build_config(thinking: str):
    from google.genai import types

    kwargs = dict(temperature=0.0, response_mime_type="application/json")
    if thinking == "none":
        kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
    elif thinking != "default":
        kwargs["thinking_config"] = types.ThinkingConfig(thinking_level=thinking.upper())
    return types.GenerateContentConfig(**kwargs)


def call_with_retry(client, modelo, contents, config, tentativas=6):
    from google.genai import errors

    espera = 5.0
    for t in range(1, tentativas + 1):
        try:
            inicio = time.perf_counter()
            resp = client.models.generate_content(model=modelo, contents=contents, config=config)
            return resp, time.perf_counter() - inicio
        except errors.APIError as e:
            if e.code in RETRY_CODES and t < tentativas:
                print(f"    API {e.code}; nova tentativa em {espera:.0f}s ({t}/{tentativas})")
                time.sleep(espera)
                espera *= 2
                continue
            raise


def custo_usd(modelo: str, entrada: int, saida: int) -> float | None:
    p = PRECOS_USD_POR_1M.get(modelo)
    if p is None:
        return None
    return (entrada * p["entrada"] + saida * p["saida"]) / 1_000_000


def p95(xs: list[float]) -> float:
    xs = sorted(xs)
    k = max(0, round(0.95 * (len(xs) - 1)))
    return xs[k]


def main() -> int:
    load_dotenv()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--modelo", required=True, help="ex.: gemini-3.6-flash")
    ap.add_argument("--thinking", default="default",
                    choices=["default", "none", "minimal", "low", "medium", "high"],
                    help="nível de raciocínio (none = thinking_budget 0, só para modelos 2.5)")
    ap.add_argument("--nome", help="nome do experimento (padrão: <modelo>-<thinking>)")
    ap.add_argument("--repeticoes", type=int, default=3,
                    help="chamadas por arquivo para medir latência; a 1ª vira a predição")
    ap.add_argument("--manifest", type=Path, default=TEST_DIR / "manifest.csv")
    ap.add_argument("--pausa", type=float, default=1.0, help="segundos entre chamadas (limite de taxa)")
    args = ap.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERRO: GEMINI_API_KEY não definida no .env", file=sys.stderr)
        return 1

    from google import genai

    nome = args.nome or f"{args.modelo}-{args.thinking}"
    pred_dir = Path("evaluation/predictions") / nome
    res_dir = Path("evaluation/results") / nome
    pred_dir.mkdir(parents=True, exist_ok=True)
    res_dir.mkdir(parents=True, exist_ok=True)

    client = genai.Client(api_key=api_key)
    try:
        client.models.get(model=args.modelo)
    except Exception as e:  # noqa: BLE001
        print(f"ERRO: modelo '{args.modelo}' indisponível para esta chave: {e}", file=sys.stderr)
        return 1

    config = build_config(args.thinking)
    prompt = PROMPT.read_text(encoding="utf-8").strip()
    base = args.manifest.parent
    with args.manifest.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["avaliado"] == "sim"]

    registros = []
    for r in rows:
        texto = (base / r["raw_text"]).read_text(encoding="utf-8")
        contents = f"{prompt}\n\nTexto para análise:\n{texto}"
        print(f"[{r['id']}]")
        for rep in range(1, args.repeticoes + 1):
            try:
                resp, lat = call_with_retry(client, args.modelo, contents, config)
            except Exception as e:  # noqa: BLE001
                print(f"    ERRO: {e}")
                if rep == 1:
                    (pred_dir / f"{r['id']}.json").write_text("", encoding="utf-8")
                registros.append({"id": r["id"], "repeticao": rep, "erro": str(e)[:300]})
                continue
            u = resp.usage_metadata
            t_in = u.prompt_token_count or 0
            t_out = u.candidates_token_count or 0
            t_think = u.thoughts_token_count or 0
            texto_resp = resp.text or ""
            if rep == 1:
                try:
                    conteudo = json.dumps(json.loads(texto_resp), ensure_ascii=False, indent=2)
                except json.JSONDecodeError:
                    conteudo = texto_resp
                (pred_dir / f"{r['id']}.json").write_text(conteudo, encoding="utf-8")
            reg = {
                "id": r["id"], "repeticao": rep, "latencia_s": round(lat, 3),
                "tokens_entrada": t_in, "tokens_saida": t_out, "tokens_raciocinio": t_think,
                "tokens_por_s": round((t_out + t_think) / lat, 1) if lat > 0 else None,
                "custo_usd": custo_usd(args.modelo, t_in, t_out + t_think), "erro": "",
            }
            registros.append(reg)
            print(f"    rep {rep}: {lat:5.1f}s | in {t_in} out {t_out} think {t_think}")
            time.sleep(args.pausa)

    ok = [x for x in registros if not x.get("erro")]
    lat = [x["latencia_s"] for x in ok]
    tps = [x["tokens_por_s"] for x in ok if x["tokens_por_s"]]
    primeira = [x for x in ok if x["repeticao"] == 1]
    custos = [x["custo_usd"] for x in primeira if x["custo_usd"] is not None]
    resumo = {
        "modelo": args.modelo, "thinking": args.thinking,
        "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "arquivos": len(rows), "repeticoes": args.repeticoes,
        "chamadas_ok": len(ok), "chamadas_com_erro": len(registros) - len(ok),
        "latencia_s": {
            "media": statistics.mean(lat) if lat else None,
            "mediana": statistics.median(lat) if lat else None,
            "p95": p95(lat) if lat else None,
        },
        "tokens_por_s_medio": statistics.mean(tps) if tps else None,
        "tokens_medios": {
            k: statistics.mean(x[f"tokens_{k}"] for x in primeira) if primeira else None
            for k in ("entrada", "saida", "raciocinio")
        },
        "custo_usd": {
            "total_17_arquivos": sum(custos) if custos else None,
            "por_programacao": statistics.mean(custos) if custos else None,
            "tabela_precos_usd_por_1M": PRECOS_USD_POR_1M.get(args.modelo),
        },
        "observacao": "Latência medida no cliente (inclui rede). Custo estimado pelos tokens da 1ª repetição.",
    }
    (res_dir / "eficiencia.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    campos = ["id", "repeticao", "latencia_s", "tokens_entrada", "tokens_saida", "tokens_raciocinio",
              "tokens_por_s", "custo_usd", "erro"]
    with (res_dir / "eficiencia.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=campos)
        w.writeheader()
        w.writerows({k: x.get(k, "") for k in campos} for x in registros)

    print(f"\nPredições em {pred_dir}  |  eficiência em {res_dir}")
    print(json.dumps(resumo["latencia_s"], indent=2))
    print(f"\nPróximo passo:\n  python -m evaluation.evaluate --pred-dir {pred_dir.as_posix()} --nome {nome}")
    return 0 if len(ok) else 1


if __name__ == "__main__":
    sys.exit(main())
