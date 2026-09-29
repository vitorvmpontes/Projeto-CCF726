# 1. Importar a biblioteca. Lembre-se, instalamos PyMuPDF, mas importamos fitz.
import fitz  # O nome da biblioteca é fitz

def extrair_texto_de_pdf(caminho_do_pdf):
    """
    Abre um arquivo PDF e extrai o texto de todas as suas páginas.

    Args:
        caminho_do_pdf (str): O caminho para o arquivo PDF.

    Returns:
        str: O texto concatenado de todas as páginas do PDF.
    """
    try:
        # 2. Abrir o arquivo PDF
        documento = fitz.open(caminho_do_pdf)
        print(f"O PDF '{caminho_do_pdf}' foi aberto com sucesso.")
        print(f"Número de páginas: {documento.page_count}")
        print("-" * 30) # Apenas uma linha para separar no console

        texto_completo = ""

        # 3. Iterar sobre cada página do documento
        # 'documento.pages()' é um método que nos permite passar por cada página
        for numero_da_pagina in range(documento.page_count):
            # Seleciona a página atual
            pagina = documento.load_page(numero_da_pagina)
            
            # 4. Extrair o texto da página
            # O método .get_text() é o coração da extração.
            # O argumento "text" garante que o resultado seja texto puro.
            texto_da_pagina = pagina.get_text("text")
            
            # Adiciona o texto da página ao nosso texto completo
            texto_completo += texto_da_pagina
            
            # Opcional: Imprimir o texto de cada página separadamente
            # print(f"--- Texto da Página {numero_da_pagina + 1} ---")
            # print(texto_da_pagina)

        # 5. Fechar o arquivo PDF após o uso
        # É uma boa prática para liberar os recursos do sistema.
        documento.close()
        
        return texto_completo

    except Exception as e:
        print(f"Ocorreu um erro ao processar o PDF: {e}")
        return None

# --- Nosso Script Principal ---
if __name__ == "__main__":
    # Defina o nome do arquivo PDF que você quer processar
    nome_do_arquivo = "../programações/wit2025/dia3.pdf"
    
    # Chama a função para extrair o texto
    texto_extraido = extrair_texto_de_pdf(nome_do_arquivo)
    
    # Verifica se a extração foi bem-sucedida
    if texto_extraido:
        print("--- CONTEÚDO COMPLETO EXTRAÍDO ---")
        print(texto_extraido)
        
        # Opcional: Salvar o texto extraído em um arquivo .txt
        with open("../textos/pyMuPDF/WIT2025/dia3.txt", "w", encoding="utf-8") as arquivo_saida:
            arquivo_saida.write(texto_extraido)
        print("\n[INFO] O texto completo foi salvo no arquivo 'texto_extraido.txt'")