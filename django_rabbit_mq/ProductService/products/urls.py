from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import ProductCategoryViewSet, ProductViewSet, ImportProducts, ImportProductCategory

app_name = "products"

router = DefaultRouter()
router.register(r"categories", ProductCategoryViewSet)
router.register(r"", ProductViewSet)

urlpatterns = [
    path(r'import-product-xml/', ImportProducts.as_view(), name='import_product_xml_api'),
    path(r'import-catergories-xml/', ImportProductCategory.as_view(), name='import_category_xml_api'),
    path("", include(router.urls)),
]
