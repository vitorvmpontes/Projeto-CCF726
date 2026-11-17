"""Roda um SLM local (llama.cpp `llama-server` ou Ollama) sobre um manifest e
salva as predições no formato do evaluate.py.

O servidor precisa expor a API compatível com OpenAI (/v1/chat/completions):

- llama.cpp (recomendado: usa o template de chat embutido no GGUF):
      llama-server -m saulin-e2b-r1.Q4_K_M.gguf --jinja -c 12288 -ngl 99 --port 8080
- Ollama:
      ollama create saulin-e2b-r1 -f Modelfile   →   --url http://localhost:11434/v1

O prompt vem de inference/prompt.py (o mesmo do treino). Decodificação gulosa
(temperatura 0), sem thinking.

Uso (na raiz do repositório):
    # validação rápida de uma rodada
    python -m evaluation.run_slm --nome e2b-r1 --manifest data/val_eval/manifest_rapido.csv
    python -m evaluation.evaluate --pred-dir evaluation/predictions/val/e2b-r1 \\
        --manifest data/val_eval/manifest_rapido.csv --nome val/e2b-r1 --pos-processar
    # teste (uma única vez, no modelo final)
    python -m evaluation.run_slm --nome e4b-final --manifest data/test/manifest.csv
"""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from inference.prompt import VERSAO_PROMPT, mensagens
from inference.schema import json_schema_saida


def chamar(url: str, modelo: str, msgs: list[dict], max_tokens: int, formato: str, timeout: float) -> tuple[dict, float]:
    corpo = {
        "model": modelo,
        "messages": msgs,
        "temperature": 0,
        "max_tokens": max_tokens,
        "stream": False,
        "chat_template_kwargs": {"enable_thinking": False},  # llama-server; ignorado pelo Ollama
    }
    if formato == "schema":
        corpo["response_format"] = {"type": "json_schema",
                                    "json_schema": {"name": "saida", "schema": json_schema_saida()}}
    elif formato == "json":
        corpo["response_format"] = {"type": "json_object"}
    req = urllib.request.Request(f"{url.rstrip('/')}/chat/completions", data=json.dumps(corpo).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        dados = json.loads(resp.read().decode("utf-8"))
    return dados, time.perf_counter() - t0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--nome", required=True, help="nome do experimento, ex.: e2b-r1")
    ap.add_argument("--manifest", type=Path, required=True)
    ap.add_argument("--url", default="http://localhost:8080/v1", help="base da API OpenAI-compatível")
    ap.add_argument("--modelo", default="local", help="nome do modelo no servidor (Ollama exige)")
    ap.add_argument("--formato", choices=["schema", "json", "livre"], default="livre",
                    help="livre = sem restrição (mede o modelo); schema = geração restrita pelo JSON Schema")
    ap.add_argument("--max-tokens", type=int, default=8192)
    ap.add_argument("--timeout", type=float, default=900)
    ap.add_argument("--refazer", action="store_true", help="refaz predições já existentes")
    args = ap.parse_args()

    teste = args.manifest.resolve().parent.name == "test"
    pred_dir = Path("evaluation/predictions") / ("" if teste else "val") / args.nome
    pred_dir.mkdir(parents=True, exist_ok=True)
    base = args.manifest.parent
    with args.manifest.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r.get("avaliado") == "sim"]

    registros = []
    for k, r in enumerate(rows, 1):
        destino = pred_dir / f"{r['id']}.json"
        if destino.exists() and not args.refazer:
            continue
        texto = (base / r["raw_text"]).read_text(encoding="utf-8")
        try:
            dados, lat = chamar(args.url, args.modelo, mensagens(texto), args.max_tokens, args.formato, args.timeout)
        except (urllib.error.URLError, TimeoutError) as e:
            print(f"[{k}/{len(rows)}] {r['id']} ERRO: {e}")
            if isinstance(e, urllib.error.URLError) and "refused" in str(e).lower():
                print("O servidor não está rodando? Veja o cabeçalho deste arquivo.", file=sys.stderr)
                return 1
            registros.append({"id": r["id"], "erro": str(e)[:300]})
            continue
        escolha = dados["choices"][0]
        conteudo = escolha["message"].get("content") or ""
        destino.write_text(conteudo, encoding="utf-8")  # saída BRUTA; o evaluate mede a validade
        u = dados.get("usage", {})
        reg = {"id": r["id"], "latencia_s": round(lat, 2), "tokens_entrada": u.get("prompt_tokens"),
               "tokens_saida": u.get("completion_tokens"), "fim": escolha.get("finish_reason"), "erro": ""}
        registros.append(reg)
        corte = "  ← CORTADO (max_tokens)" if reg["fim"] == "length" else ""
        print(f"[{k}/{len(rows)}] {r['id']}: {lat:5.1f}s | in {reg['tokens_entrada']} out {reg['tokens_saida']}{corte}")

    ok = [x for x in registros if not x["erro"]]
    if ok:
        lat = [x["latencia_s"] for x in ok]
        resumo = {
            "nome": args.nome, "manifest": args.manifest.as_posix(), "url": args.url, "formato": args.formato,
            "versao_prompt": VERSAO_PROMPT, "gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "chamadas": len(registros), "erros": len(registros) - len(ok),
            "cortadas_max_tokens": sum(1 for x in ok if x["fim"] == "length"),
            "latencia_s": {"media": statistics.mean(lat), "mediana": statistics.median(lat)},
            "registros": registros,
        }
        (pred_dir / "_execucao.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nPredições em {pred_dir}/ ({len(ok)} novas, {len(registros) - len(ok)} erros)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
