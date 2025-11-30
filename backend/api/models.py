from django.core.validators import MinValueValidator
from django.db import models
import uuid


class BaseModel(models.Model):
    uuid = models.UUIDField(
            primary_key=True,
            default=uuid.uuid4,
            editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Expense(BaseModel):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name="paying_user")
    contributors = models.ManyToManyField('auth.User', through='Contribution')
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    is_settled = models.BooleanField(default=False)


class Contribution(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE)
    contributor = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
