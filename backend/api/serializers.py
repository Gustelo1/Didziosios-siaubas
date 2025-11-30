from decimal import Decimal

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


class ContributionNestedSerializer(serializers.ModelSerializer):
    contributor_id = serializers.IntegerField(required=False)

    class Meta:
        model = Contribution
        fields = ("id", "contributor_id", "amount")


class ContributionSerializer(serializers.ModelSerializer):
    contributor_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Contribution
        fields = ("id", "expense", "contributor_id", "amount")
        extra_kwargs = {"expense": {"read_only": True}}


class ExpenseSerializer(serializers.ModelSerializer):
    contributions = ContributionNestedSerializer(many=True, source='contribution_set')

    class Meta:
        model = Expense
        fields = (
            "uuid",
            "owner",
            "title",
            "amount",
            "contributions",
            "created_at",
        )

    def create(self, validated_data):
        contributions = validated_data.pop('contribution_set')
        expense = Expense.objects.create(**validated_data)
        for contribution in contributions:
            Contribution.objects.create(
                expense=expense,
                contributor_id=contribution['contributor_id'],
                amount=contribution['amount']
            )
        return expense

    def update(self, instance, validated_data):
        contributions_data = validated_data.pop("contribution_set", None)

        instance = super().update(instance, validated_data)

        if contributions_data is not None:
            instance.contribution_set.all().delete()

            for c in contributions_data:
                Contribution.objects.create(
                    expense=instance,
                    contributor_id=c["contributor_id"],
                    amount=c["amount"]
                )

        return instance


    def validate(self, data):
        data = super().validate(data)
        full_price = data.get("amount")
        all_contributions_price = Decimal("0")
        if contributions := data.get("contribution_set"):
            for contribution in contributions:
                all_contributions_price += contribution.get("amount")

            if full_price != all_contributions_price:
                raise serializers.ValidationError(f"Contributions sum {all_contributions_price} does not match expense price {full_price}. \n Difference: {full_price - all_contributions_price}.")

        return data
