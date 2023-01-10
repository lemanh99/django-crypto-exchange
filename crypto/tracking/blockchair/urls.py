from django.urls import path

from crypto.tracking.blockchair import views

urlpatterns = [
    path('number_request', views.get_information_request, name='get_information_request'),
    path('ethereum/history-transaction', views.get_history_transaction, name='get_history_transaction'),
    path('ethereum/analysis-token-by-exchange', views.get_analysis_token_by_exchange,
         name='get_analysis_token_by_exchange'),
]
