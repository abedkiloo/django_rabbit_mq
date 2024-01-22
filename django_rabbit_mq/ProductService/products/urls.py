from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import ProductCategoryViewSet, ProductViewSet, ImportProducts

app_name = "products"

router = DefaultRouter()
router.register(r"categories", ProductCategoryViewSet)
router.register(r"", ProductViewSet)

urlpatterns = [
    path(r'import-xml/', ImportProducts.as_view(), name='import_xml_api'),
    path("", include(router.urls)),
]
