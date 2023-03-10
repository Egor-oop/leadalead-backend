"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include

from rest_framework import routers

from apps.users.views import UserDetail, RegisterUserAPIView, CustomAuthToken
from apps.projectsapp.views import ProjectViewSet
from apps.leadsapp.views import LeadViewSet

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'leads', LeadViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('account/<pk>/detail', UserDetail.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('login/', CustomAuthToken.as_view()),
]
