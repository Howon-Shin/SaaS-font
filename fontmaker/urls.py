from django.urls import path
from fontmaker import views


urlpatterns = [
    path('', views.intro, name='intro'),
    path('draw/<int:pk>/', views.draw, name='draw'),
]