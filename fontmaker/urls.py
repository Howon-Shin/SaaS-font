from django.urls import path
from fontmaker import views


urlpatterns = [
    path('', views.index, name='index'),
    path('draw/<int:pk>/', views.draw, name='draw'),
    path('draw/<int:pk>/saveImg/', views.draw_save_img, name='saveImg'),
    path('draw/<int:pk>/<str:letter>/', views.draw_load_img, name='loadImg'),
]