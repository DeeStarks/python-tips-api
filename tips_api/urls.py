from django.urls import path
from . import views

urlpatterns = [
    path('tips', views.fetch_tips, name='fetch_tips'),
    path('tips/<int:tip_id>', views.fetch_tip, name='fetch_tip'),
    path('tips/add', views.add_tip, name='add_tip'),
]