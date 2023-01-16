from django.urls import path

from crypto.coinglass import views

urlpatterns = [
    path('funding-rate', views.get_funding_rate, name='get_funding_rate'),
]
