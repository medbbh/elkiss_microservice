from django.urls import path
from .views import *

urlpatterns = [
    path("", UserTransactionsAPIView.as_view(), name="user-transactions"),
    path("donate/", DonateAPIView.as_view(), name="donate"),
    path("cagnottes/<str:pk>/transactions/", FundTransactionsAPIView.as_view(), name="cagnotte-transactions"),
]