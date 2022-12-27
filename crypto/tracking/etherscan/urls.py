from django.urls import path

from crypto.tracking.etherscan import views

urlpatterns = [
    path('contact-abi-veryfy', views.get_contact_verify, name='get_contact_verify'),
]
