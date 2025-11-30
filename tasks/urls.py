from django.urls import path
from . import views

urlpatterns = [
    path('api/tasks/analyze/', views.analyze, name='analyze'),
    path('api/tasks/suggest/', views.suggest, name='suggest'),
]
