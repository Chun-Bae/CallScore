"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from config.views import login
from config.views import loading
from config.views import get_score
from config.views import del_score
from callscore.views import viewScores

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',login),
    path('loading/',loading, name='loading'),
    path('view/',viewScores, name='viewScores'),
    path('get_score/', get_score, name='get_score'),
    path('del_score/', del_score, name='del_score'),
]

urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)
