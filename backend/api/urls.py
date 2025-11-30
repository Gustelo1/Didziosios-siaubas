from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import ExpenseView, ContributionCreateView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r"expense", ExpenseView, basename="expense")

urlpatterns = [
    path("", include(router.urls)),
    path("expense/<uuid:expense_pk>/add-contributor", ContributionCreateView.as_view(), name="add-contributor")
]