from django.urls import path
from . import views

urlpatterns = [
    path('tips', views.fetch_tips),
    path('tips/<int:tip_id>', views.fetch_tip),
]