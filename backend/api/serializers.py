from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Expense, Contribution


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'password',
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contribution
        fields = ("amount", "contributor")


class ExpenseSerializer(serializers.ModelSerializer):
    contributions = ContributionSerializer(many=True, write_only=True)

    class Meta:
        model = Expense
        fields = ("owner", "title", "price", "contributions", "created_at")

    def create(self, validated_data):
        contributions_data = validated_data.pop("contributions")
        expense = Expense.objects.create(**validated_data)

        for c in contributions_data:
            Contribution.objects.create(expense=expense, **c)

        return expense
