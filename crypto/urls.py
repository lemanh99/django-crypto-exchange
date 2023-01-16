"""crypto URL Configuration

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
from django.urls import path, include
from drf_spectacular.views import SpectacularSwaggerView, SpectacularRedocView, SpectacularAPIView

urlpatterns = [
    path(
        '',
        SpectacularSwaggerView.as_view(
            template_name='swagger-ui.html',
            url_name="schema"
        ),
        name="swagger-ui",
    ),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='re-doc'),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path('api/v1/biance/', include('crypto.binance.urls')),
    path('api/v1/poloniex/', include('crypto.poloniex.urls')),
    path('api/v1/coingecko/', include('crypto.coingecko.urls')),
    path('api/v1/tracking/', include('crypto.tracking.urls')),
    path('api/v1/coinglass/', include('crypto.coinglass.urls')),
    path('api/v1/user/', include('crypto.user.urls')),
]
