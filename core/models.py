from django.db import models

class Rotulo(models.Model): 
    rotulo = models.ImageField(upload_to='images/') 