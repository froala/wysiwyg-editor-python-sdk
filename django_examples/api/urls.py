from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload_file', views.upload_file, name='upload_file'),
    url(r'^upload_image', views.upload_image, name='upload_image'),
    url(r'^delete_file', views.delete_file, name='delete_file'),
    url(r'^delete_image', views.delete_image, name='delete_image'),
    url(r'^load_images', views.load_images, name='load_images'),
]