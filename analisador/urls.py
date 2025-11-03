# Em analisador/urls.py

from django.urls import path
from . import views  # Importa as views do app 'analisador'

# Este 'apelido' é importante para a tag {% url %} nos templates
app_name = 'analisador'

urlpatterns = [
    # Quando a URL estiver "vazia" (raiz do app),
    # chame a função 'analyze_image_view' do nosso views.py
    # Dê a ela o nome (apelido) 'analise_upload'
    path('', views.analyze_image_view, name='analise_upload'),
]