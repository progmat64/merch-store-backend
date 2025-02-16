from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Inventory, MerchItem, Transaction, User


class InfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        inventory = Inventory.objects.filter(user=user).values(
            "merch_item__name", "quantity"
        )
        received = Transaction.objects.filter(to_user=user).values(
            "from_user__username", "amount"
        )
        sent = Transaction.objects.filter(from_user=user).values(
            "to_user__username", "amount"
        )

        return Response(
            {
                "coins": user.coins,
                "inventory": list(inventory),
                "coinHistory": {
                    "received": list(received),
                    "sent": list(sent),
                },
            }
        )


class BuyMerchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item):
        user = request.user
        merch = get_object_or_404(MerchItem, name=item)

        if user.coins < merch.price:
            return Response(
                {"error": "Недостаточно монет"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.coins -= merch.price
        user.save()

        inventory, _ = Inventory.objects.get_or_create(
            user=user, merch_item=merch
        )
        inventory.quantity += 1
        inventory.save()

        return Response({"message": "Товар куплен"}, status=status.HTTP_200_OK)


class SendCoinsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        from_user = request.user
        to_username = request.data.get("toUser")
        amount = int(request.data.get("amount", 0))

        to_user = get_object_or_404(User, username=to_username)

        if amount <= 0 or from_user.coins < amount:
            return Response(
                {"error": "Недостаточно монет или некорректная сумма"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        from_user.coins -= amount
        to_user.coins += amount
        from_user.save()
        to_user.save()

        Transaction.objects.create(
            from_user=from_user, to_user=to_user, amount=amount
        )

        return Response(
            {"message": "Монеты отправлены"}, status=status.HTTP_200_OK
        )
