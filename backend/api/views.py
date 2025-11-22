from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from api.models import Expense
from api.serializers import UserSerializer, ExpenseSerializer


class UserCreateView(CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny,]
    queryset = User.objects.all()


class ExpenseView(ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny,]
    queryset = Expense.objects.all()
