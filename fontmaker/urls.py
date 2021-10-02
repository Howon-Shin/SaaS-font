from django.urls import path
from fontmaker import views


urlpatterns = [
    path('', views.index, name='index'),
    path('draw/<int:pk>/', views.draw, name='draw'),
    path('draw/<int:pk>/saveImg/', views.draw_save_img, name='saveImg'),
    path('draw/<int:pk>/undone/', views.undone_chars, name='undone'),
    path('draw/<int:pk>/deleteProj/', views.delete_project, name='deleteProj'),
    path('draw/<int:pk>/exitProj/', views.exit_project, name='exitProj'),
    path('draw/<int:pk>/inviteMember/', views.invite_member, name='inviteMember'),
    path('draw/<int:pk>/manageMember/', views.manage_member, name='manageMember'),
    path('draw/<int:pk>/fireMember/', views.fire_member, name='fireMember'),
    path('draw/<int:pk>/<str:letter>/', views.draw_load_img, name='loadImg'),
]
