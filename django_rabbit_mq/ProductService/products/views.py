from rest_framework import permissions, viewsets

from products.models import Product, ProductCategory
from products.permissions import IsSellerOrAdmin
from products.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def __init__(self):
        self.permission_classes = None

    def get_serializer_class(self):
        if self.action.lower() in ('create', 'update', 'partial_update', 'destroy'):
            return ProductWriteSerializer
        return ProductReadSerializer

    def get_permissions(self):
        if self.action.lower() in ('create',):
            self.permission_classes = (permissions.IsAuthenticated,)
        if self.action.lower() in ('update', 'partial_update', 'destroy',):
            self.permission_classes = (IsSellerOrAdmin,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()
