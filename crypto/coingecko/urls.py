from django.urls import path

from crypto.coingecko import views

urlpatterns = [
    path('get-percent-market-exchange', views.get_percent_market_exchange, name='get_percent_market_exchange'),
    path('<str:blockchain_ecosystem>/get-coin-exchange-market', views.get_coin_exchange_market, name='get_coin_exchange_dex'),
    path('<str:exchange_id>/get-coin-exchange-dex', views.get_coin_exchange_dex, name='get_coin_exchange_dex'),
    path('<str:exchange_id>/get-address-token', views.get_address_token_by_exchange_id, name='get_address_token_by_exchange_id'),
    path('<str:contract_address>/verify-chain-erc20', views.get_verify_chain_erc20, name='get_verify_chain_erc20'),
    path('get-same-coin', views.get_same_coin, name='get_same_coin'),
]
