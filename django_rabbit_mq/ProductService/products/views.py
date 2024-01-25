import os
from django.conf import settings

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


class ImportProductCategory(APIView):

    def post(self, request, ):
        try:
            product_xml = request.FILES.get('product_category')
            if not product_xml:
                return Response({"error": "NO valid Category XML provided"}, status=status.HTTP_400_BAD_REQUEST)

            tree = ET.parse(product_xml)
            root = tree.getroot()

            for item in root.findall('category'):
                category_name = item.find('name').text
                prd_category = ProductCategory.objects.get_or_create(name=category_name)
            return Response({"success": "OK"}, status=status.HTTP_200_OK)
        except Exception as exception:
            return Response({'error': str(exception)}, status=400)


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
                name, desc, quantity, price, category = item.find('name').text, item.find('desc').text, item.find(
                    'quantity').text, item.find('price').text, item.find('category')
                imported_data.append({name, desc, quantity, price, category})
                instance, created = ProductCategory.objects.get_or_create(category)

                product = Product(name=name, desc=desc, quantity=quantity, price=price, category=instance)
                product.save()
            return Response(imported_data, status=status.HTTP_200_OK)
        except ET.ParseError:
            return Response({"error": "Invalid XML"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An error {str(e)} occurred"}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        product_object = ProductReadSerializer(products, many=True)
        product_list = product_object.data
        write_to_xml = self.write_to_xml(product_list)
        return Response({"products": write_to_xml}, status=status.HTTP_200_OK)

    def write_to_xml(self, product_object):

        root_element = ET.Element('products_data')
        for product_item in product_object:
            product_element = ET.Element('products')
            for key, value in product_item.items():
                ET.SubElement(product_element, key).text = str(value)
            root_element.append(product_element)

        relative_path = 'product_files/products.xml'

        # Combine the base directory and relative path to form the complete file path
        file_path = os.path.join(settings.BASE_DIR, relative_path)

        # Ensure the directory exists before saving the file
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # Save the XML content to the file
        with open(file_path, 'wb') as file:
            file.write(ET.tostring(root_element))

        return {'message': 'Products exported to XML file successfully.'}


def read_xm_products(xml_file_path):
    try:
        with open(xml_file_path, 'r') as xml_file:
            xml_data = xml_file.read()
        headers = {"Content-Type": 'application/xml'}
    except FileNotFoundError:
        print("File Not Found")
