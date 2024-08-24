from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Computer, Part, Game, Cart, Shop


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ComputerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Computer
        fields = ['name', 'year_of_creation', 'date_of_sell', 'supplier', 'firm', 'state', 'address', 'description', 'price']
class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    parts = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Part.objects.all(),
        required=False
    )

    class Meta:
        model = Cart
        fields = ['id', 'user', 'parts', 'total_price', 'date_of_payment']
        read_only_fields = ['total_price', 'date_of_payment']
        
class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
