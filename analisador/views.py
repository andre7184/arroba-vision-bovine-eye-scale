# Em analisador/views.py

from django.shortcuts import render
from .forms import ImageUploadForm  # Nosso formulário da TASK-003
from .roboflow_utils import get_model_predictions # Nosso cérebro da TASK-004
from .analysis_utils import process_predictions  # Nossa lógica de cálculo da TASK-006.2

def analyze_image_view(request):
    """
    View principal que lida com o upload e a análise da imagem.
    """
    
    # Contexto inicial para a página (para o formulário)
    context = {
        'form': ImageUploadForm()
    }

    # Se o usuário enviou o formulário (método POST)
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        
        # O Django verifica se o arquivo é válido (ex: é uma imagem)
        if form.is_valid():
            uploaded_image = request.FILES['image']
            
            # 1. Chamar a IA (TASK-004)
            # 'predictions' será o JSON com os dados, ou None se der erro
            # 'error' será a msg de erro, ou None se der certo
            predictions, error = get_model_predictions(uploaded_image)
            
            print(f"predictions: {predictions}")  # Apenas para debug
            print(f"error: {error}")
            print("----")
            print("----")


            if error:
                # Se a API do Roboflow falhar (sem créditos, API key errada, etc.)
                context['error'] = f"Erro na API do Roboflow: {str(error)}"
                # Envia o erro para a página de resultado
                return render(request, 'analisador/resultado.html', context)
            
            # 2. Chamar a Lógica de Cálculo (TASK-006.2)
            # Este é o bloco de "tentativa"
            try:
                print(predictions)  # Apenas para debug
                # Esta função vai calcular a proporção, idade e peso
                calculation_results = process_predictions(predictions)
                
                # 'update' adiciona todos os resultados (peso, idade, etc.) ao context
                context.update(calculation_results)
                
                # Mostra a página de sucesso COM os resultados
                return render(request, 'analisador/resultado.html', context)
                
            except ValueError as e:
                # Se o 'process_predictions' falhar (ex: não achou olho)
                # ESTA É A LINHA CRÍTICA PARA O SEU BUG:
                context['error'] = f"Erro no processamento: {str(e)}"
                
                # Mostra a página de resultado no MODO DE ERRO
                return render(request, 'analisador/resultado.html', context)
        
        else:
            # Se o formulário não for válido (ex: não é imagem)
            # O 'form' agora contém as mensagens de erro e será exibido
            context['form'] = form

    # Se for um GET (primeira visita à página) ou se o formulário for inválido,
    # mostra a página de upload.
    return render(request, 'analisador/upload.html', context)