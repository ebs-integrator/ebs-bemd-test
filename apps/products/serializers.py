from datetime import date

from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from apps.products.models import Product, PriceInterval


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class PriceIntervalSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceInterval
        fields = '__all__'

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("start_date can not be bigger than end_date.")
        return data

    def validate_end_date(self, value):
        if not value:
            return date.max
        return value


class ProductStatsSerializer(serializers.Serializer):
    product = PrimaryKeyRelatedField(queryset=Product.objects.all(), required=True)
    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)
