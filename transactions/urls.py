from django.urls import path
from .views import *

urlpatterns = [
    path("", UserTransactionsAPIView.as_view(), name="user-transactions"),
    path("cagnottes/<str:pk>/", FundTransactionsAPIView.as_view(), name="cagnotte-transactions"),
]