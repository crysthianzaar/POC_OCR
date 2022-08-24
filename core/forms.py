from django import forms
from .models import *


class RotuloForm(forms.ModelForm):
    rotulo = forms.ImageField(label='Selecione uma imagem')

    class Meta:
        model = Rotulo
        fields = ['rotulo']
