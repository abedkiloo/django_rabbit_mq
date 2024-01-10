from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Product
from .product_producer import ProductProducer

User = get_user_model()

product_producer = ProductProducer()


@receiver(post_save, sender=User)
def create_product(sender, instance, created, **kwargs):
    print("Product Created")
    if created:
        created_product = Product.objects.create(user=instance)
        product_producer.publish("product_created_method", created_product)
