from drf_util.views import BaseViewSet, BaseCreateModelMixin, BaseListModelMixin
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.products.models import Product, PriceInterval
from apps.products.serializers import ProductSerializer, PriceIntervalSerializer, ProductStatsSerializer
from apps.products.utils.price_counter import Prices
from apps.products.utils.price_validator import PriceValidator


class ProductViewSet(BaseListModelMixin, BaseCreateModelMixin, BaseViewSet):
    permission_classes = AllowAny,
    authentication_classes = ()
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @action(detail=False, methods=['GET'])
    def stats(self, request, *args, **kwargs):
        serializer = ProductStatsSerializer(data=request.query_params)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        average_prices = Prices(serializer.validated_data)
        average_prices.get_average()
        return Response(average_prices, status=status.HTTP_200_OK)


class ProductPriceViewSet(BaseListModelMixin, BaseCreateModelMixin, BaseViewSet):
    permission_classes = AllowAny,
    authentication_classes = ()
    serializer_class = PriceIntervalSerializer
    queryset = PriceInterval.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        interval_inserter = PriceValidator(serializer, self.queryset)
        interval_inserter.insert_price()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

