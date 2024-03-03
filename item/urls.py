from django.urls import path

from item.views import StripeSessionIdRetrieveAPIVIew, BuyRetrieve


urlpatterns = [
    path("item/<int:pk>/", StripeSessionIdRetrieveAPIVIew.as_view(), name="item"),
    path("buy/<int:pk>/", BuyRetrieve.as_view())
]
