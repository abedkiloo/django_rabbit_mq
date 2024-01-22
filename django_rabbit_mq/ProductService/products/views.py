from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from xml.etree import ElementTree as ET
from rest_framework import status

from rest_framework.parsers import MultiPartParser
from products.models import Product, ProductCategory
from products.permissions import IsSellerOrAdmin
from products.serializers import (
    ProductCategoryReadSerializer,
    ProductReadSerializer,
    ProductWriteSerializer,
)


class ProductCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and Retrieve product categories
    """

    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategoryReadSerializer
    permission_classes = (permissions.AllowAny,)


class ProductViewSet(viewsets.ModelViewSet):
    """
    CRUD products
    """

    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update", "destroy"):
            return ProductWriteSerializer

        return ProductReadSerializer

    def get_permissions(self):
        # if self.action in ("create",):
        #     self.permission_classes = (permissions.IsAuthenticated,)
        if self.action in ("update", "partial_update", "destroy"):
            self.permission_classes = (IsSellerOrAdmin,)
        else:
            self.permission_classes = (permissions.AllowAny,)

        return super().get_permissions()


class ImportProducts(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        try:
            uploaded_file = request.FILES.get("products")
            if not uploaded_file:
                return Response({"error": "XML File was not provided"}, status=status.HTTP_400_BAD_REQUEST)

            tree = ET.parse(uploaded_file)
            root = tree.getroot()


            imported_data = []
            for item in root.findall('product'):
                name, desc, quantity, price = item.find('name').text, item.find('desc').text, item.find(
                    'quantity').text, item.find('price').text
                imported_data.append([name, desc, quantity, price])
            return Response(imported_data, status=status.HTTP_200_OK)
        except ET.ParseError:
            return Response({"error": "Invalid XML"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error {str(e)} occurred"}, status=status.HTTP_400_BAD_REQUEST)


def read_xm_products(xml_file_path):
    try:
        with open(xml_file_path, 'r') as xml_file:
            xml_data = xml_file.read()
        headers = {"Content-Type": 'application/xml'}
    except FileNotFoundError:
        print("File Not Found")
