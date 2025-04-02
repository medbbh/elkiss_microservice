from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users.views import CountryListView, CustomTokenObtainPairView, LogoutView, RegisterView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("countries/", CountryListView.as_view(), name="country-list"),

]
