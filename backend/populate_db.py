import os
import django

# IMPORTANT: this must go first
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

import random
from django.contrib.auth.models import User
from api.models import Expense, Contribution

# 1. Create 20 users
users = []
for i in range(20):
    username = f"user_{i + 1}"
    email = f"{username}@example.com"
    user = User.objects.create_user(username=username, email=email, password="password123")
    users.append(user)

# 2. Create 20 expenses
expenses = []
for i in range(20):
    owner = random.choice(users)
    title = f"Expense {i + 1}"
    amount = round(random.uniform(10, 500), 2)
    expense = Expense.objects.create(owner=owner, title=title, amount=amount)
    expenses.append(expense)

# 3. Create contributions for each expense
for expense in expenses:
    num_contributors = random.randint(2, 5)

    # Pick distinct users for contributors
    contributors = random.sample(users, num_contributors)

    remaining_amount = float(expense.amount)

    for idx, contributor in enumerate(contributors):
        if idx == len(contributors) - 1:
            amount = remaining_amount  # Last one gets whatever is left
        else:
            # Ensure valid remaining range
            max_amount = remaining_amount - (len(contributors) - idx - 1)
            amount = round(random.uniform(1, max_amount), 2)
            remaining_amount -= amount

        Contribution.objects.create(
            expense=expense,
            contributor=contributor,
            amount=amount
        )

print("Successfully populated Users, Expenses, and Contributions!")
