from django.shortcuts import render
from rest_framework import generics, status
from django.views import generic
import stripe
from rest_framework.response import Response

from config import settings
from item.serializers import ItemSerializer
from item.models import Item
from item.stipes_requests import get_checkout


class StripeSessionIdRetrieveAPIVIew(generics.RetrieveAPIView):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # serializer = self.get_serializer(instance)
        domain = request.META.get("HTTP_HOST")
        data = {"domain": domain, "item": instance}
        checkout_session_result = get_checkout(data)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        return Response(checkout_session_result)


class BuyRetrieve(generic.DetailView):
    model = Item
    template_name = "home.html"
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        instance = self.get_object()
        domain = self.request.META.get("HTTP_HOST")
        data = {"domain": domain, "item": instance}
        checkout_session_result = get_checkout(data)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        context = super().get_context_data(**kwargs)
        context["result"] = checkout_session_result
        return context
