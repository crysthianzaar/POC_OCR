from django import forms
from .models import *


class RotuloForm(forms.ModelForm):
    rotulo = forms.ImageField(label='Selecione uma imagem')

    class Meta:
        model = Rotulo
        fields = ['rotulo']

class DadosForm(forms.ModelForm):
    meter = forms.CharField()
    lote = forms.CharField()
    artikel = forms.CharField()

    class Meta:
        model = DadosRotulo
        fields = ['meter','lote','artikel']