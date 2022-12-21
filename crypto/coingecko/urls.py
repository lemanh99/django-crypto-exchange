from django.urls import path

from crypto.coingecko import views

urlpatterns = [
    path('get-percent-market-exchange', views.get_percent_market_exchange, name='get_percent_market_exchange'),
    path('<str:blockchain_ecosystem>/get-coin-exchange-market', views.get_coin_exchange_market, name='get_coin_exchange_dex'),
    path('<str:exchange_id>/get-coin-exchange-dex', views.get_coin_exchange_dex, name='get_coin_exchange_dex'),
]
