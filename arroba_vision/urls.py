# Em nome_do_projeto/urls.py

from django.contrib import admin
# 1. Adicione 'include' aqui
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),

    # 2. Adicione esta linha:
    # Ela diz ao Django: "Para qualquer URL (o ''), 
    # inclua (include) o arquivo de URLs do nosso app 'analisador'".
    path('', include('analisador.urls')),
]