from django.db import models

class Rotulo(models.Model): 
    id_rotulo = models.AutoField(primary_key=True)
    rotulo = models.ImageField(upload_to='images/') 

class DadosRotulo(models.Model):
    id_dados = models.AutoField(primary_key=True)
    meter = models.CharField(max_length=100)
    lote = models.CharField(max_length=100)
    artikel = models.CharField(max_length=100)

class Image(models.Model):
    image = models.ImageField(upload_to='images')