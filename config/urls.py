"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from config.ddtb import DEBUG_TOOLBAR_PATH

from freelance.views import RegisterView
from ratings.views import RatingListView, RatingUpdateView

urlpatterns = [
    path('', include('freelance.urls')),
    path('', include('ratings.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    DEBUG_TOOLBAR_PATH, 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

