# extractors.py
import base64
import requests
import fitz 
from abc import ABC, abstractmethod

class BaseExtractor(ABC):
    """Classe base abstrata para todos os extratores."""
    @abstractmethod
    def extract(self, file_path: str) -> str:
        pass

class ImageExtractor(BaseExtractor):
    """Extrai texto de arquivos de imagem (PNG, JPG) usando a Google Vision API."""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"

    def extract(self, file_path: str) -> str:
        print(f"-> Extraindo texto da imagem '{file_path}' com Google Vision...")
        try:
            with open(file_path, "rb") as image_file:
                my_base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        except FileNotFoundError:
            print(f"ERRO: Arquivo de imagem não encontrado em '{file_path}'.")
            return None

        payload = {
            "requests": [{"image": {"content": my_base64_string}, "features": [{"type": "DOCUMENT_TEXT_DETECTION"}]}]
        }

        response = requests.post(self.url, json=payload)

        if response.status_code == 200:
            result = response.json()
            try:
                detected_text = result['responses'][0]['textAnnotations'][0]['description']
                print("-> Texto extraído com sucesso.")
                return detected_text
            except (KeyError, IndexError):
                print("AVISO: Nenhum texto foi detectado na imagem.")
                return ""
        else:
            print(f"ERRO: A requisição para a Vision API falhou com o status {response.status_code}")
            print("Resposta da API:", response.text)
            return None

class PDFExtractor(BaseExtractor):
    """Extrai texto de arquivos PDF usando PyMuPDF (fitz) para alta performance."""
    def extract(self, file_path: str) -> str:
        print(f"-> Extraindo texto do PDF '{file_path}' com PyMuPDF (fitz)...")
        full_text = ""
        try:
            
            with fitz.open(file_path) as doc:
                print(f"   - O documento tem {len(doc)} páginas.")
                for i, page in enumerate(doc):
                    print(f"   - Processando página {i+1}...")
                    
                    page_text = page.get_text("text")
                    
                    if page_text:
                       
                        full_text += page_text
                        
                print("-> Texto extraído com sucesso.")
                return full_text
        except Exception as e:
            print(f"ERRO: Falha ao processar o PDF '{file_path}' com PyMuPDF. Detalhes: {e}")
            return None