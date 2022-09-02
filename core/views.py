import base64
from pyexpat import model
from tempfile import NamedTemporaryFile
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import DadosRotulo, Rotulo
from .forms import DadosForm, RotuloForm
from django.http import JsonResponse
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
import environ
from PIL import Image
import os
import shutil
import glob
import cv2
import pytesseract

from core import models

env = environ.Env()
environ.Env.read_env()

def index(request):
    return render(request, 'index.html')

def call_camera(request):
    return render(request, 'image.html')

def scanner(request):
    form = DadosForm(request.POST)
    if form.is_valid():
           novo_rotulo = form.save(commit=False)
           novo_rotulo.save()
           return redirect('/')
    return render(request, 'form.html', {'form': form})

def camera(request):

    if request.method == 'POST':
        form = RotuloForm(request.POST, request.FILES)
        form.save()
        path = os.getcwd() + "/media/images/*"
        try:
            for path_to_license_plate in glob.glob(path, recursive=True):
                img = cv2.imread(path_to_license_plate, cv2.IMREAD_GRAYSCALE)
                cv2.dilate(img, (5, 5), img)
                pytesseract.pytesseract.tesseract_cmd = env(
                    'OCR_ENGINE_DIRECTORY')
                string = pytesseract.image_to_string(img)
                try:
                    meter = tratamento_meter(string)
                    lote = tratamento_lote(string)
                    artikel = tratamento_artikel(string)
                except:
                    pass

                delete()

                form_dados = DadosForm(request.POST)
                if form_dados.is_valid():
                    DadosRotulo.objects.create(
                        meter=meter,
                        lote=lote,
                        artikel=artikel
                    )
                
                form_result = DadosForm(initial={'meter': meter,'lote': lote, 'artikel': artikel })

            return render(request, 'form_result.html', {'form': form_result})
        except:
            return JsonResponse({'message': 'Erro: parâmetros não identificados', 'retorno_ocr': string})
    else:
        form = RotuloForm()
    return render(request, 'base.html', {'form': form})


def image_upload(request):
    if request.method== 'POST':        
       img = request.POST.get("photo").replace('data:image/png;base64,', '')
       image_file_like = base64.b64decode(img)
       f = open("temp.JPEG", "wb")
       f.write(image_file_like)
       f.close()
       img = cv2.imread("temp.JPEG", cv2.IMREAD_GRAYSCALE)
       cv2.dilate(img, (5, 5), img)
       pytesseract.pytesseract.tesseract_cmd = env(
            'OCR_ENGINE_DIRECTORY')
       string = pytesseract.image_to_string(img)
       print(string)
    try:
        meter = tratamento_meter(string)
        lote = tratamento_lote(string)
        artikel = tratamento_artikel(string)
    except:
        pass
    try:
        DadosRotulo.objects.create(
            meter=meter,
            lote=lote,
            artikel=artikel
        )
    
        form_result = DadosForm(initial={'meter': meter,'lote': lote, 'artikel': artikel })

        return render(request, 'form_result.html', {'form': form_result})
    except:
        context = {'string': string}
        return render(request, 'error.html',context=context)
    

    

def delete():
    try:
        folder = os.getcwd() + '/media/images'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    except:
        pass


def tratamento_meter(string: str) -> int:

    meter = string[string.rfind("Meter"):string.rfind("Date"):]
    meter = int(''.join(i for i in meter if i.isdigit()))
    n = str(meter)

    # Tratativas de caracteres
    meter = str(n.replace('9', '0'))
    meter = int(meter)

    return meter


def tratamento_lote(string: str) -> int:

    lote = string[string.rfind("Lot"):string.rfind("Ar"):]
    lote = int(''.join(i for i in lote if i.isdigit()))
    return lote


def tratamento_artikel(string: str) -> int:

    artikel = string[string.rfind("Ar"):string.rfind("Meter"):]
    artikel = int(''.join(i for i in artikel if i.isdigit()))
    return artikel
