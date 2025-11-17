from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.serializers import UserSerializer


# Create your views here.
class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.all()