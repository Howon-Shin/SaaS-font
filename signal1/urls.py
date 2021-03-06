"""signal1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.urls import path
from fontmaker import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('fontmaker/', include('fontmaker.urls')),
    path('', RedirectView.as_view(url='/fontmaker/', permanent=True)),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('newProject/', views.new_project, name='newProj'),
    path('existProject/', views.exist_project, name='existProj'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
