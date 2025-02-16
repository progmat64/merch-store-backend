from rest_framework import serializers
from .models import User, MerchItem, Transaction, Purchase, Inventory

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'coins']

class MerchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchItem
        fields = ['id', 'name', 'price']

class TransactionSerializer(serializers.ModelSerializer):
    from_user = serializers.StringRelatedField()
    to_user = serializers.StringRelatedField()

    class Meta:
        model = Transaction
        fields = ['id', 'from_user', 'to_user', 'amount', 'timestamp']

class PurchaseSerializer(serializers.ModelSerializer):
    merch_item = serializers.StringRelatedField()

    class Meta:
        model = Purchase
        fields = ['id', 'user', 'merch_item', 'quantity', 'timestamp']

class InventorySerializer(serializers.ModelSerializer):
    merch_item = MerchItemSerializer()

    class Meta:
        model = Inventory
        fields = ['id', 'merch_item', 'quantity']
