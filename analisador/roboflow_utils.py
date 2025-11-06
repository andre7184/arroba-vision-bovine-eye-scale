# Em analisador/roboflow_utils.py

import requests  # Para fazer a chamada de internet
import base64    # Para codificar a imagem
from django.conf import settings # Para pegar nossas chaves secretas

def get_model_predictions(uploaded_image):
    """
    Envia uma imagem (UploadedFile do Django) para a API do Roboflow 
    e retorna o JSON das predições.
    """

    # --- 1. Preparar a Imagem ---
    # Ler os dados da imagem em memória
    image_data = uploaded_image.read()

    # Codificar a imagem em Base64, que é como a API do Roboflow espera.
    # .decode('utf-8') transforma os bytes em uma string de texto.
    image_base64 = base64.b64encode(image_data).decode('utf-8')

    # --- 2. Preparar a Chamada da API ---
    # Montar a URL completa (ex: https://detect.roboflow.com/meu-modelo/2)
    api_url = f"{settings.ROBOFLOW_API_URL}{settings.ROBOFLOW_MODEL_ID}"

    # Parâmetros da URL, incluindo nossa chave secreta
    params = {
        'api_key': settings.ROBOFLOW_API_KEY,
        # (Opcional) Você pode adicionar outros params se quiser
        # 'confidence': 40, # Ex: só retornar predições acima de 40%
        # 'overlap': 30,    # Ex: % de sobreposição
    }

    # --- 3. Fazer a Requisição (A "Mágica") ---
    # Nós enviamos os dados da imagem (image_base64) no corpo (data) da requisição.
    response = requests.post(
        api_url,
        params=params,
        data=image_base64,
        headers={'Content-Type': 'application/x-www-form-urlencoded'}
    )

    # --- 4. Tratar a Resposta ---
    if response.status_code == 200:
        # Sucesso! A IA nos deu uma resposta.
        # response.json() converte a resposta de texto em um dicionário Python
        return response.json(), None  # (dados_das_predições, nenhum_erro)
    else:
        # Algo deu errado (sem créditos, API key errada, etc.)
        # response.json() provavelmente conterá a mensagem de erro
        return None, response.json() # (nenhum_dado, dados_do_erro)