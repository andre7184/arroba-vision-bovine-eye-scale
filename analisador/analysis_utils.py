# Em analisador/analysis_utils.py
# (TASK-006.2 - Versão CORRIGIDA)

import json
import os
from django.conf import settings # Para encontrar nosso arquivo JSON

# Carregar a base de conhecimento UMA VEZ quando o app iniciar
# Isso é muito mais eficiente do que ler o arquivo a cada requisição
json_path = os.path.join(settings.BASE_DIR, 'analisador', 'breed_data.json')
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        BREED_DATA = json.load(f)
except FileNotFoundError:
    # Se o arquivo não existir, criamos um fallback
    print("AVISO: breed_data.json não encontrado. Usando dados de fallback.")
    BREED_DATA = {
        "nelore": { "nome_exibicao": "Nelore", "bezerro_ratio_max": 950, 
                    "adulto_ratio_min": 1050, "k_factor_bezerro": 0.45, "k_factor_adulto": 0.60 }
    }


def calculate_area(prediction):
    """Função auxiliar para calcular a área em pixels de uma caixa (bounding box)."""
    return prediction['width'] * prediction['height']


def estimate_age_and_weight(proporcao, breed_key="nelore"):
    """
    Usa a proporção para estimar a idade e o peso.
    """
    if breed_key not in BREED_DATA:
        raise ValueError(f"Dados da raça '{breed_key}' não encontrados no JSON.")
        
    data = BREED_DATA[breed_key]
    
    # Lógica de decisão para idade
    if proporcao <= data['bezerro_ratio_max']:
        idade_estimada = "Bezerro"
        k_factor = data['k_factor_bezerro']
    elif proporcao >= data['adulto_ratio_min']:
        idade_estimada = "Adulto"
        k_factor = data['k_factor_adulto']
    else:
        idade_estimada = "Novilha / Garrote (intermediário)"
        # Usar uma média dos fatores K
        k_factor = (data['k_factor_bezerro'] + data['k_factor_adulto']) / 2
        
    # Fórmula final do peso!
    peso_estimado = proporcao * k_factor
    
    return idade_estimada, round(peso_estimado, 1)


def process_predictions(predictions_data):
    """
    Processa o JSON bruto da API, calcula tudo (incluindo idade e peso)
    e retorna um dicionário com os resultados.
    
    Levanta um ValueError se os dados necessários não forem encontrados.
    """
    
    olhos = []
    corpos = []

    # 1. Separar as predições por classe
    #    (ESTA É A CORREÇÃO CRÍTICA)
    for pred in predictions_data.get('predictions', []):
        if pred['class'] == 'olho-boi':    # <-- CORRIGIDO para hífen
            olhos.append(pred)
        elif pred['class'] == 'corpo-boi':  # <-- CORRIGIDO para hífen
            corpos.append(pred)
    
    # 2. Validar se encontramos o que precisávamos
    # Se o modelo não encontrou nenhum corpo, levantamos um erro
    if not corpos:
        raise ValueError("O modelo não conseguiu detectar um 'corpo-boi' na imagem.")
    
    # Se o modelo não encontrou nenhum olho, levantamos um erro
    if not olhos:
        raise ValueError("O modelo não conseguiu detectar um 'olho-boi' na imagem.")

    # 3. Escolher a "melhor" detecção
    # Escolhe a detecção com a maior 'confiança'.
    best_corpo = max(corpos, key=lambda p: p['confidence'])
    best_olho = max(olhos, key=lambda p: p['confidence'])

    # 4. Calcular áreas e proporção
    area_corpo = calculate_area(best_corpo)
    area_olho = calculate_area(best_olho)

    if area_olho == 0:
        raise ValueError("A área do olho detectada é zero, impossível calcular proporção.")

    proporcao = area_corpo / area_olho
    
    # 5. CHAMAR A NOVA LÓGICA (SUA IDEIA!)
    # Por enquanto, estamos "forçando" a raça Nelore.
    idade_estimada, peso_estimado = estimate_age_and_weight(proporcao, breed_key="nelore")

    # 6. Retornar um dicionário limpo para a view
    return {
        'area_corpo': int(area_corpo),
        'area_olho': int(area_olho),
        'proporcao': round(proporcao, 2),
        'idade_estimada': idade_estimada,
        'peso_estimado': peso_estimado,
        'confidence_corpo': round(best_corpo['confidence'] * 100, 1),
        'confidence_olho': round(best_olho['confidence'] * 100, 1),
        'predictions_json': predictions_data # Para nosso debug no HTML
    }