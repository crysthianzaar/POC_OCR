from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', index),
    path('image', image_upload, name='image_upload'),
    path('camera', camera,name="call_camera"),
    path('scanner', scanner, name='scanner'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
