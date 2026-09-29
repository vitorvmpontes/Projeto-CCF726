import google.generativeai as genai

class GeminiService:
    """Serviço para interagir com a API do Google Gemini."""
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-pro-latest')

    def get_json_from_text(self, extracted_text: str, prompt_template: str) -> str:
        """Monta o prompt final, define a instrução de sistema e chama a LLM."""
        print("-> Enviando texto para a LLM com Instrução de Sistema...")
        
        system_instruction = (
            "Você é um robô de extração de dados altamente preciso e especializado. "
            "Sua única função é analisar o texto fornecido pelo usuário e convertê-lo "
            "em um formato JSON, seguindo estritamente as regras, a estrutura e o exemplo fornecidos. "
            "Não adicione comentários, saudações ou qualquer texto fora do JSON solicitado. "
            "Seja literal e preciso."
        )

        user_prompt = f"{prompt_template}\n\n--- TEXTO EXTRAÍDO PARA ANÁLISE ---\n\n{extracted_text}"

        generation_config = genai.GenerationConfig(
            temperature=0.1,
        )

        try:
            
            response = self.model.generate_content(
                [system_instruction, user_prompt], 
                generation_config=generation_config
            )
            
            json_response = self._clean_response(response.text)
            print("-> JSON recebido e formatado com sucesso.")
            return json_response
        except Exception as e:
            print(f"ERRO: Falha ao chamar a API do Gemini. Detalhes: {e}")
            return None

    def _clean_response(self, text: str) -> str:
        """Remove os marcadores de código e espaços extras da resposta da LLM."""
        start = text.find('[')
        if start == -1:
            start = text.find('{')

        end = text.rfind(']')
        if end == -1:
            end = text.rfind('}')

        if start != -1 and end != -1:
            return text[start:end+1]
        return text