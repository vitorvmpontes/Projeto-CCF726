import json
import os
import re
from typing import List, Dict, Tuple, Any, Optional
import datetime

# --- Configuração ---
# Agora definimos os diretórios RAIZ (principais)
BASE_GROUND_TRUTH_DIR = "../Manual"
BASE_LLM_OUTPUTS_DIR = "../IA"
# O relatório bruto será salvo no diretório onde o script for executado
RAW_RESULTS_FILE = "relatorio_bruto_agregado.json"
# O arquivo CSV será salvo no diretório onde o script for executado
CSV_RESULTS_FILE = "relatorio_metricas_por_arquivo.csv"
# --------------------


def normalize_text(text: Any) -> str:
    """
    Normaliza o texto para uma comparação mais robusta.
    Converte para minúsculas e remove espaços em branco no início/fim.
    Lida com entradas que não são string (como null/None).
    """
    if not isinstance(text, str):
        return ""
    return text.lower().strip()


def compare_descriptions(gt_desc: str, pred_desc: str) -> bool:
    """
    Compara duas descrições de forma inteligente.
    Remove tags HTML e normaliza o texto antes de comparar.
    """
    gt_clean = re.sub('<[^<]+?>', '', gt_desc) if gt_desc else ''
    pred_clean = re.sub('<[^<]+?>', '', pred_desc) if pred_desc else ''
    
    return normalize_text(gt_clean) == normalize_text(pred_clean)


def compare_activities(ground_truth_activities: List[Dict], predicted_activities: List[Dict]) -> Tuple[int, int, int, Dict[str, int]]:
    """
    Compara duas listas de atividades e calcula TP, FP, FN, e a contagem de campos corretos.
    (Lógica idêntica à sua)
    """
    tp = 0
    field_correct_counts = {'nome': 0, 'lugar': 0, 'dataInicio': 0, 'dataFim': 0, 'descricao': 0}
    
    predicted_copy = list(predicted_activities)
    gt_copy = list(ground_truth_activities)

    for pred_activity in list(predicted_copy):
        pred_nome_norm = normalize_text(pred_activity.get("nome"))
        
        match_found_in_gt = None
        for gt_activity in gt_copy:
            gt_nome_norm = normalize_text(gt_activity.get("nome"))
            
            if pred_nome_norm and pred_nome_norm == gt_nome_norm:
                match_found_in_gt = gt_activity
                break
        
        if match_found_in_gt:
            tp += 1
            field_correct_counts['nome'] += 1
            
            if normalize_text(pred_activity.get("lugar")) == normalize_text(match_found_in_gt.get("lugar")):
                field_correct_counts['lugar'] += 1
            if normalize_text(pred_activity.get("dataInicio")) == normalize_text(match_found_in_gt.get("dataInicio")):
                field_correct_counts['dataInicio'] += 1
            if normalize_text(pred_activity.get("dataFim")) == normalize_text(match_found_in_gt.get("dataFim")):
                field_correct_counts['dataFim'] += 1
            if compare_descriptions(match_found_in_gt.get("descricao"), pred_activity.get("descricao")):
                field_correct_counts['descricao'] += 1
            
            predicted_copy.remove(pred_activity)
            gt_copy.remove(match_found_in_gt)
            
    fp = len(predicted_copy)
    fn = len(gt_copy)
    
    return tp, fp, fn, field_correct_counts


def processar_par_de_arquivos(gt_path: str, pred_path: str, filename_display: str) -> Dict[str, Any]:
    """
    Processa um único par de arquivos (GT e Predição) e retorna um dicionário 
    com os contadores brutos (TP, FP, FN, etc.) e o status.
    Agora inclui 'total_atividades_gt' para contagem global.
    """
    resultado_arquivo = {
        "arquivo": filename_display,
        "status": "erro",
        "mensagem": "",
        "tp": 0,
        "fp": 0,
        "fn": 0,
        "total_atividades_gt": 0,  # Novo campo
        "field_counts": {'nome': 0, 'lugar': 0, 'dataInicio': 0, 'dataFim': 0, 'descricao': 0}
    }

    try:
        if not os.path.exists(gt_path):
             resultado_arquivo["mensagem"] = f"Arquivo ground truth não encontrado em {gt_path}"
             return resultado_arquivo

        # Carrega GT para contar atividades mesmo se a predição falhar
        with open(gt_path, 'r', encoding='utf-8') as f:
            gt_activities = json.load(f)
        
        if isinstance(gt_activities, list):
            resultado_arquivo["total_atividades_gt"] = len(gt_activities)
        else:
             resultado_arquivo["mensagem"] = "Arquivo Ground Truth não é uma lista JSON."
             return resultado_arquivo

        # Lógica para lidar com arquivos de predição ausentes
        if not os.path.exists(pred_path):
            resultado_arquivo["mensagem"] = "Arquivo de predição correspondente não encontrado."
            resultado_arquivo["fn"] = len(gt_activities)
            resultado_arquivo["status"] = "sucesso_sem_predicao"
            return resultado_arquivo

        with open(pred_path, 'r', encoding='utf-8') as f:
            pred_activities = json.load(f)

        if not isinstance(pred_activities, list):
            resultado_arquivo["mensagem"] = "Arquivo de Predição não é uma lista JSON. Contando como Falsos Positivos."
            resultado_arquivo["status"] = "sucesso_predicao_invalida"
            resultado_arquivo["fn"] = len(gt_activities)
            resultado_arquivo["fp"] = 0
            return resultado_arquivo


        tp, fp, fn, field_counts = compare_activities(gt_activities, pred_activities)
        
        resultado_arquivo["status"] = "sucesso"
        resultado_arquivo["tp"] = tp
        resultado_arquivo["fp"] = fp
        resultado_arquivo["fn"] = fn
        resultado_arquivo["field_counts"] = field_counts
        
    except json.JSONDecodeError as e:
        resultado_arquivo["mensagem"] = f"Erro ao decodificar JSON: {e}"
    except Exception as e:
        resultado_arquivo["mensagem"] = f"Erro inesperado: {e}"
    
    return resultado_arquivo


def calcular_metricas(tp: int, fp: int, fn: int) -> Tuple[float, float, float]:
    """Calcula Precision, Recall e F1 Score dado TP, FP e FN."""
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


def gerar_relatorio_final(resultados_brutos: List[Dict[str, Any]]):
    """
    Recebe a lista de resultados brutos de cada arquivo, gera o relatório
    final agregado no console E imprime uma tabela detalhada por arquivo.
    Também salva em CSV.
    """
    total_tp, total_fp, total_fn = 0, 0, 0
    total_atividades_dataset = 0  # Variável para acumular o total de atividades
    total_field_correct = {'nome': 0, 'lugar': 0, 'dataInicio': 0, 'dataFim': 0, 'descricao': 0}
    arquivos_com_erro = 0
    arquivos_processados_com_sucesso = 0
    
    tabela_detalhada = []
    header = [
        "Arquivo", "Total_Ativ_GT", "TP", "FP", "FN", "Precision", "Recall", "F1-Score", 
        "Acc_Nome", "Acc_Lugar", "Acc_DataIni", "Acc_DataFim", "Acc_Desc"
    ]
    tabela_detalhada.append(header)

    for res in resultados_brutos:
        # Consideramos sucesso qualquer status que permitiu ler o GT (mesmo sem predição)
        if "sucesso" in res["status"]:
            arquivos_processados_com_sucesso += 1
            
            tp = res["tp"]
            fp = res["fp"]
            fn = res["fn"]
            ativ_gt = res.get("total_atividades_gt", 0)
            f_counts = res.get("field_counts", {})

            # Acumular totais
            total_tp += tp
            total_fp += fp
            total_fn += fn
            total_atividades_dataset += ativ_gt
            
            for field, count in f_counts.items():
                total_field_correct[field] += count
            
            prec, rec, f1 = calcular_metricas(tp, fp, fn)

            acc_nome = f_counts.get('nome', 0) / tp if tp > 0 else 0.0
            acc_lugar = f_counts.get('lugar', 0) / tp if tp > 0 else 0.0
            acc_data_ini = f_counts.get('dataInicio', 0) / tp if tp > 0 else 0.0
            acc_data_fim = f_counts.get('dataFim', 0) / tp if tp > 0 else 0.0
            acc_desc = f_counts.get('descricao', 0) / tp if tp > 0 else 0.0

            linha = [
                res["arquivo"],
                ativ_gt, # Adicionado na tabela
                tp, fp, fn,
                f"{prec:.2%}", f"{rec:.2%}", f"{f1:.4f}",
                f"{acc_nome:.2%}", f"{acc_lugar:.2%}", f"{acc_data_ini:.2%}", f"{acc_data_fim:.2%}", f"{acc_desc:.2%}"
            ]
            tabela_detalhada.append(linha)

        else:
            arquivos_com_erro += 1
            linha_erro = [res["arquivo"], "ERRO", "ERRO", "ERRO", "ERRO", "-", "-", "-", "-", "-", "-", "-", "-"]
            tabela_detalhada.append(linha_erro)

    # --- IMPRESSÃO DA TABELA NO CONSOLE ---
    print("\n" + "="*150)
    print(f"{'TABELA DETALHADA POR ARQUIVO':^150}")
    print("="*150)
    
    # Ajustei o formato para incluir a nova coluna "Total_Ativ_GT"
    row_format = "{:<40} | {:>6} | {:>4} | {:>4} | {:>4} | {:>8} | {:>8} | {:>8} | {:>8} | {:>8} | {:>8} | {:>8} | {:>8}"
    
    print(row_format.format(*header))
    print("-" * 150)
    
    for row in tabela_detalhada[1:]:
        if row[1] == "ERRO":
             print(row_format.format(*row))
        else:
            print(row_format.format(*row))
    print("="*150)


    # --- RELATÓRIO GLOBAL (AGREGADO) ---
    print("\n" + "="*50)
    print("--- RELATÓRIO FINAL CONSOLIDADO ---")
    print(f"Gerado em: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total de arquivos processados: {arquivos_processados_com_sucesso}")
    print(f"Total de arquivos com erro: {arquivos_com_erro}")
    print("-" * 50)
    print(f"TOTAL DE ATIVIDADES NO DATASET (Ground Truth): {total_atividades_dataset}")
    print("="*50)

    print("\n--- Nível 1: Desempenho na Detecção de Atividades (GLOBAL) ---")
    print(f"Total TP: {total_tp}")
    print(f"Total FP: {total_fp}")
    print(f"Total FN: {total_fn}")
    
    g_prec, g_rec, g_f1 = calcular_metricas(total_tp, total_fp, total_fn)
    
    print(f"\nPrecisão: {g_prec:.2%}")
    print(f"Recall: {g_rec:.2%}")
    print(f"F1-Score: {g_f1:.4f}")

    print("\n--- Nível 2: Acurácia por Campo (GLOBAL) ---")
    if total_tp > 0:
        for field, count in total_field_correct.items():
            accuracy = count / total_tp
            print(f"Acurácia '{field}': {accuracy:.2%} ({count}/{total_tp})")
    else:
        print("Nenhum TP encontrado.")
        
    print("\n" + "="*50)
    
    # --- SALVAR CSV ---
    print(f"\nSalvando tabela em '{CSV_RESULTS_FILE}'...")
    try:
        with open(CSV_RESULTS_FILE, 'w', encoding='utf-8') as f:
            f.write(";".join(header) + "\n")
            for row in tabela_detalhada[1:]:
                f.write(";".join(map(str, row)) + "\n")
        print("CSV salvo com sucesso.")
    except Exception as e:
        print(f"ERRO ao salvar CSV: {e}")


# --- FUNÇÃO MAIN (INALTERADA) ---

def main():
    print("--- Iniciando Script de Validação Completo ---")
    
    if not os.path.isdir(BASE_GROUND_TRUTH_DIR):
        print(f"ERRO: Diretório GT não encontrado: {BASE_GROUND_TRUTH_DIR}")
        return
    if not os.path.isdir(BASE_LLM_OUTPUTS_DIR):
        print(f"ERRO: Diretório LLM não encontrado: {BASE_LLM_OUTPUTS_DIR}")
        return

    pares_de_arquivos = []

    print(f"Varrendo '{BASE_GROUND_TRUTH_DIR}'...")
    for dirpath, dirnames, filenames in os.walk(BASE_GROUND_TRUTH_DIR):
        for filename in filenames:
            if filename.endswith('.json'):
                gt_path = os.path.join(dirpath, filename)
                relative_dir = os.path.relpath(dirpath, BASE_GROUND_TRUTH_DIR)
                pred_path = os.path.join(BASE_LLM_OUTPUTS_DIR, relative_dir, filename)
                display_name = os.path.join(relative_dir, filename)
                pares_de_arquivos.append((gt_path, pred_path, display_name))

    if not pares_de_arquivos:
        print("Nenhum arquivo .json encontrado.")
        return
    
    print(f"Arquivos encontrados: {len(pares_de_arquivos)}")
    
    resultados_brutos = []
    
    for i, (gt_path, pred_path, display_name) in enumerate(pares_de_arquivos):
        # Feedback visual simples
        # print(f"Processando {i+1}/{len(pares_de_arquivos)}: {display_name}") 
        
        resultado = processar_par_de_arquivos(gt_path, pred_path, display_name) 
        resultados_brutos.append(resultado)

    gerar_relatorio_final(resultados_brutos)


if __name__ == "__main__":
    main()