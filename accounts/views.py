from .models import Account
from .serializers import AccountSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404


class AccountView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

