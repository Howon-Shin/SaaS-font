from django.urls import path
from fontmaker import views


urlpatterns = [
    path('', views.index, name='index'),
    path('draw/<int:pk>/', views.draw, name='draw'),
]