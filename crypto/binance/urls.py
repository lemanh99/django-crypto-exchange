from django.urls import path, include

from crypto.binance import views

urlpatterns = [
    path('account-information', views.binance_account_information, name='binance_account_information'),
    path('funding-rate', views.get_funding_rate_binance, name='get_funding_rate_binance'),
]
