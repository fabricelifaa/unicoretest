"""unicorerestapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import include, path
from rest_framework import routers
from unicoretest.views import Register_user, Login, Get_keys, Logout, Get_restaurants


router = routers.DefaultRouter()
# router.register('users', views.UserViewSet)

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('unicore/register/', Register_user),
    path('unicore/api_keys/', Get_keys),
    path('unicore/login/', Login),
    path('unicore/logout/', Logout),
    path('unicore/restaurants/', Get_restaurants),
]
