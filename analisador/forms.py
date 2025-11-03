# Em analisador/forms.py
from django import forms

class ImageUploadForm(forms.Form):
    """
    Um formulário simples para lidar com o upload de uma única imagem.
    """
    image = forms.ImageField(
        label="Selecione a foto do boi",
        help_text="Envie uma imagem (.jpg, .png) para análise."
    )