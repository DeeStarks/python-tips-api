from django.urls import path
from . import views

urlpatterns = [
    path('tips/all', views.fetchall),
]