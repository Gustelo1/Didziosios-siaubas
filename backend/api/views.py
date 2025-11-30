from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Expense, Contribution
from api.serializers import UserSerializer, ExpenseSerializer, ContributionSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()


class ExpenseView(ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [AllowAny,]
    queryset = Expense.objects.all()


class ContributionCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ContributionSerializer

    def create(self, request, *args, **kwargs):
        expense_uuid = self.kwargs.get('expense_pk')

        try:
            expense_obj = Expense.objects.get(uuid=expense_uuid)
        except Expense.DoesNotExist:
            return Response(
                {"error": "Expense not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        existing_contribution = expense_obj.contribution_set.filter(
            contributor=serializer.validated_data['contributor']
        ).first()

        if existing_contribution:
            existing_contribution.amount += serializer.validated_data['amount']
            existing_contribution.save()
        else:
             Contribution.objects.create(
                expense=expense_obj,
                contributor=serializer.validated_data['contributor'],
                amount=serializer.validated_data['amount']
            )

        return Response(
            "success",
            status=status.HTTP_201_CREATED
        )

