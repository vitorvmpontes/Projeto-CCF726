import ollama
import re
import json

client = ollama.Client()

model = 'saulin_v2:latest'
userprompt = ''
context = [] 

# Carrega o seu prompt de regras (P1.txt / prompt.txt)
with open('prompt.txt', 'r', encoding='utf-8') as f:
    base_prompt = f.read().strip()

print("--- Extrator de Atividades Técnico Iniciado ---")
print("Digite 'sair' para encerrar o programa.\n")

while userprompt != 'sair':
    userprompt = input("Cole o texto bruto da programação: ")
    if userprompt.lower() == "sair":
        break
    else:
        # Mescla suas instruções de sistema com a string bruta fornecida pelo usuário
        combined_prompt = f"{base_prompt}\n\nTexto para análise:\n{userprompt}" if base_prompt else userprompt
        
        print("\nProcessando e estruturando dados (Aguarde)...")
        
        try:
            response = client.generate(
                model=model,
                prompt=combined_prompt,
                context=context,
                format='json', # Força estruturação gramatical estrita em nível de token
                options={
                    'temperature': 0.0 # Garante determinismo total exigido pelo JSON Schema
                }
            )
            
            # Atualiza o contexto histórico da conversa no loop
            context = response.context 
            raw_output = response.response
            
            # --- Tratamento de Segurança para Modelos de Raciocínio (DeepSeek-R1) ---
            # Remove a cadeia de pensamento (<think>...</think>) se ela vier misturada no output
            json_clean = re.sub(r'<think>.*?</think>', '', raw_output, flags=re.DOTALL).strip()
            
            # Validação e embelezamento do JSON antes de exibir no terminal
            json_parsed = json.loads(json_clean)
            json_formatted = json.dumps(json_parsed, indent=2, ensure_ascii=False)
            
            print("\n=== JSON DE ATIVIDADES EXTRAÍDO ===")
            print(json_formatted)
            print("===================================\n")
            
        except json.JSONDecodeError:
            # Caso ocorra alguma inconsistência crítica de formatação
            print("\n[Erro]: Não foi possível realizar o parse completo do objeto retornado.")
            print("Resposta bruta capturada:\n", raw_output, "\n")
        except Exception as e:
            print(f"\n[Erro inesperado]: {e}\n")