from django.urls import path
from . import views
from django.http import HttpResponse
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_file, name='upload_file'),
    path('process_url/', views.process_url, name='process_url'),
    path('chat/', views.chat_with_ai, name='chat_with_ai'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
]
