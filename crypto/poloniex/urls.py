from django.urls import path

from crypto.poloniex import views

urlpatterns = [
    path('get-pair-trade', views.get_pair_trade_arbitrage, name='get_pair_trade_arbitrage'),
    path('trade-arbitrage', views.trade_arbitrage, name='trade_arbitrage'),
]
