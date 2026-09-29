import os
import json
import argparse
import config
from extractors import ImageExtractor, PDFExtractor
from llm_service import GeminiService

def main(input_path: str):
    """Função principal que orquestra todo o pipeline de extração."""
    print("="*50)
    print("--- INICIANDO PIPELINE DE EXTRAÇÃO DE ATIVIDADES ---")
    print("="*50)
    
    try:
        with open("prompt.txt", "r", encoding="utf-8") as f:
            prompt_template = f.read()
    except FileNotFoundError:
        print("ERRO: Arquivo 'prompt.txt' não encontrado.")
        return

    _, file_extension = os.path.splitext(input_path)
    file_extension = file_extension.lower()

    extractor = None
    if file_extension in ['.png', '.jpg', '.jpeg']:
        extractor = ImageExtractor(api_key=config.GOOGLE_VISION_API_KEY)
    elif file_extension == '.pdf':
        extractor = PDFExtractor()
    else:
        print(f"ERRO: Formato de arquivo '{file_extension}' não suportado.")
        return

    extracted_text = extractor.extract(input_path)
    
    if not extracted_text:
        print("Pipeline encerrado: não foi possível extrair texto do arquivo.")
        return

    gemini_service = GeminiService(api_key=config.GEMINI_API_KEY)
    structured_json_str = gemini_service.get_json_from_text(extracted_text, prompt_template)
    print(extracted_text)

    if not structured_json_str:
        print("Pipeline encerrado: não foi possível obter o JSON da LLM.")
        return

    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    filename_stem = os.path.splitext(os.path.basename(input_path))[0]

    output_filename = os.path.join(output_dir, f"{filename_stem}_output.json")
    try:
        json_data = json.loads(structured_json_str)
        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        print("\n" + "="*50)
        print(f"O resultado foi salvo em: {output_filename}")
        print("="*50)
    except json.JSONDecodeError:
        print(f"ERRO: A saída da LLM não é um JSON válido. Salvando como texto bruto.")
        raw_output_filename = os.path.join(output_dir, f"{filename_stem}_output_raw.txt")
        with open(raw_output_filename, "w", encoding="utf-8") as f:
            f.write(structured_json_str)
        print(f"Saída bruta salva em: {raw_output_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extrai e estrutura atividades de um arquivo de programação.")
    parser.add_argument("input_file", type=str, help="O caminho para o arquivo de entrada (.pdf, .png, .jpg)")
    args = parser.parse_args()
    
    main(args.input_file)