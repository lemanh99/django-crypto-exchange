from django.urls import path

from crypto.coingecko import views

urlpatterns = [
    path('get-percent-market-exchange', views.get_percent_market_exchange, name='get_percent_market_exchange'),
]
