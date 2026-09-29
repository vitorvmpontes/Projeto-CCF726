import json
import os
from typing import List, Dict, Any

GROUND_TRUTH_DIR = "../Manual/WIT2025/"
LLM_OUTPUTS_DIR = "../IA/WIT2025/"



def normalize_text(text: Any) -> str:
    """
    Normaliza o texto para uma comparação mais robusta.
    Converte para minúsculas e remove espaços em branco no início/fim.
    Lida com entradas que não são string (como null/None).
    """
    if not isinstance(text, str):
        return ""
    return text.lower().strip()


def find_and_log_field_errors(gt_activities: List[Dict], pred_activities: List[Dict], filename: str) -> int:
    """
    Encontra atividades correspondentes usando um algoritmo de melhor correspondência
    e registra discrepâncias nos campos de data.
    """
    error_count = 0
    
    # Cria uma cópia da lista do gabarito para poder remover itens com segurança
    gt_copy = list(gt_activities)

    for pred_activity in pred_activities:
        best_match = None
        best_match_score = 0 # 0 = sem match, 1 = match por nome, 2 = match perfeito

        # Procura a melhor correspondência para a atividade prevista na lista do gabarito
        for gt_activity in gt_copy:
            pred_nome = normalize_text(pred_activity.get("nome"))
            gt_nome = normalize_text(gt_activity.get("nome"))
            
            if pred_nome == gt_nome:
                # Encontrou um match pelo nome (score mínimo de 1)
                current_score = 1
                
                pred_inicio = normalize_text(pred_activity.get("dataInicio"))
                gt_inicio = normalize_text(gt_activity.get("dataInicio"))

                if pred_inicio == gt_inicio:
                    # Encontrou um match perfeito (nome + dataInicio)
                    current_score = 2
                
                if current_score > best_match_score:
                    best_match_score = current_score
                    best_match = gt_activity

                # Se já encontrou um match perfeito, não precisa procurar mais para esta pred_activity
                if best_match_score == 2:
                    break
        
        # Se uma correspondência foi encontrada, analisa os campos e remove o item do gabarito
        if best_match:
            # Remove a correspondência da lista do gabarito para não ser usada novamente
            gt_copy.remove(best_match)
            
            # Agora, com o par correto, checa os campos de data para erros
            gt_inicio = best_match.get('dataInicio')
            pred_inicio = pred_activity.get('dataInicio')
            if normalize_text(gt_inicio) != normalize_text(pred_inicio):
                error_count += 1
                print("-" * 50)
                print("ERRO DE CAMPO DETECTADO")
                print(f"  - Arquivo:     {filename}")
                print(f"  - Atividade:   {best_match.get('nome')}")
                print(f"  - Campo:       dataInicio")
                print(f"  - Esperado (GT): {gt_inicio}")
                print(f"  - Recebido (LLM):{pred_inicio}")

            gt_fim = best_match.get('dataFim')
            pred_fim = pred_activity.get('dataFim')
            if normalize_text(gt_fim) != normalize_text(pred_fim):
                error_count += 1
                print("-" * 50)
                print("ERRO DE CAMPO DETECTADO")
                print(f"  - Arquivo:     {filename}")
                print(f"  - Atividade:   {best_match.get('nome')}")
                print(f"  - Campo:       dataFim")
                print(f"  - Esperado (GT): {gt_fim}")
                print(f"  - Recebido (LLM):{pred_fim}")

    return error_count


def main():
    """
    Função principal que orquestra o processo de investigação de erros.
    """
    print("--- Iniciando Script de Investigação de Erros (Versão Refinada) ---")
    
    total_errors_found = 0
    
    if not os.path.isdir(GROUND_TRUTH_DIR):
        print(f"ERRO: Diretório de ground truth não encontrado em '{GROUND_TRUTH_DIR}'")
        return

    ground_truth_files = [f for f in os.listdir(GROUND_TRUTH_DIR) if f.endswith('.json')]
    
    if not ground_truth_files:
        print(f"AVISO: Nenhum arquivo .json encontrado em '{GROUND_TRUTH_DIR}'")
        return

    for filename in ground_truth_files:
        gt_path = os.path.join(GROUND_TRUTH_DIR, filename)
        pred_path = os.path.join(LLM_OUTPUTS_DIR, filename)
        
        if not os.path.exists(pred_path):
            continue
            
        try:
            with open(gt_path, 'r', encoding='utf-8') as f:
                gt_activities = json.load(f)
            with open(pred_path, 'r', encoding='utf-8') as f:
                pred_activities = json.load(f)

            if not isinstance(gt_activities, list) or not isinstance(pred_activities, list):
                print(f"\nAVISO: Conteúdo em '{filename}' não é uma lista. Pulando.")
                continue

            total_errors_found += find_and_log_field_errors(gt_activities, pred_activities, filename)
            
        except Exception as e:
            print(f"\nERRO: Falha ao processar o arquivo {filename}. Detalhes: {e}")

    print("\n" + "="*50)
    print("--- INVESTIGAÇÃO CONCLUÍDA ---")
    print(f"Total de erros de campo ('dataInicio' e 'dataFim') encontrados: {total_errors_found}")
    print("Use o log acima para categorizar os tipos de erro.")
    print("="*50)


if __name__ == "__main__":
    main()