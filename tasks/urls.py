from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/tasks/analyze/', views.analyze, name='analyze'),
    path('api/tasks/suggest/', views.suggest, name='suggest'),
]
