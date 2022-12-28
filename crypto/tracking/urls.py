from django.urls import path, include

from crypto.poloniex import views

urlpatterns = [
    path('etherscan/', include('crypto.tracking.etherscan.urls')),
]
