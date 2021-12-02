import random
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from faker import Faker
from products.models import Product, Status
import faker.providers


PRODUCT_STATUSES = ["Active", "Out Of Stock", "Temporarily Not Available"]


class Provider(faker.providers.BaseProvider):
    def product_status(self, product_status=None):
        if product_status is None:
            product_status = PRODUCT_STATUSES
        return self.random_element(product_status)


class Command(BaseCommand):
    help = "DB SEEDER"

    def handle(self, *args, **kwargs):

        Status.objects.all().delete()
        Product.objects.all().delete()
        fake = Faker()
        fake.add_provider(Provider)

        for _ in range(len(PRODUCT_STATUSES)):
            s = fake.unique.product_status()
            Status.objects.create(text=s)

        active_product_statuses = tuple(
            Status.objects.all().values_list('text', flat=True))
        products = []
        for i in range(300):
            product_name = f"Num {i} Product"
            s = fake.product_status(active_product_statuses)
            s = Status.objects.get(text=s)
            price = random.randint(100, 25000)
            slug = slugify(product_name)
            product = (product_name, s, price, slug)
            products.append(product)
        Product.objects.bulk_create(
            Product(name=name, status=status, price=price, slug=slug) for name, status, price, slug in products)

        self.stdout.write(self.style.SUCCESS(
            f"Seeding Complete!\nCategories Created: {len(active_product_statuses)}\nProducts Created: {len(products)}"))
