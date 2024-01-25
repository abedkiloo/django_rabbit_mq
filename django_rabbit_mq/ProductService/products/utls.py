from rest_framework_xml.renderers import XMLRenderer


class ProductXMLRendererclass(XMLRenderer):
    root_tag_name = 'product_categories'
    item_tag_name = 'categories'
