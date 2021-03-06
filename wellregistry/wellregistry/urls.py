"""wellregistry URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path


urlpatterns = [
    # this is the django admin url which allows adding django users and table management
    path('registry/admin/', admin.site.urls),
    path('registry/chaining/', include('smart_selects.urls')),

    path('registry/', include('social_django.urls', namespace='social')),
    path('registry/accounts/', include('django.contrib.auth.urls')),

    # this is our registry page
    path('registry/', include('registry.urls')),
]
urlpatterns += staticfiles_urlpatterns()
