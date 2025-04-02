from django.urls import path
from .views import DonateAPIView, FundListCreateAPIView, FundRetrieveUpdateDestroyAPIView, CloseFundAPIView

urlpatterns = [
    path("cagnottes/", FundListCreateAPIView.as_view(), name="cagnotte-list-create"),
    path("cagnottes/<str:pk>/", FundRetrieveUpdateDestroyAPIView.as_view(), name="cagnotte-detail"),
    path("cagnottes/<str:pk>/close/", CloseFundAPIView.as_view(), name="cagnotte-close"),
    # path("cagnottes/<str:pk>/open/", OpenFundAPIView.as_view(), name="cagnotte-open"),

    path("donate/", DonateAPIView.as_view(), name="donate"),

]