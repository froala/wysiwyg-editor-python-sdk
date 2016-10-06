from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload_file', views.upload_file, name='upload_file'),
    url(r'^upload_image', views.upload_image, name='upload_image'),
    url(r'^load_images', views.load_images, name='load_images'),
]