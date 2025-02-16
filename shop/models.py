from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    coins = models.IntegerField(default=1000)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="shop_users",
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="shop_users_permissions",
        blank=True,
    )


class MerchItem(models.Model):
    name = models.CharField(max_length=50, unique=True)
    price = models.IntegerField()


class Inventory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merch_item = models.ForeignKey(MerchItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)


class Transaction(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_transactions",
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_transactions"
    )
    amount = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merch_item = models.ForeignKey(MerchItem, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
