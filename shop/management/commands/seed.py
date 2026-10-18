from django.core.management.base import BaseCommand
from shop.models import Product

SAMPLE = [
    ('Wireless Headphones', 'Over-ear Bluetooth headphones with 30-hour battery life.', 2499, 15),
    ('Mechanical Keyboard', 'Compact RGB keyboard with tactile blue switches.', 3299, 10),
    ('Smart Watch', 'Fitness tracking, heart-rate monitor and notifications.', 4999, 8),
    ('Laptop Backpack', 'Water-resistant backpack with a padded 15.6" laptop sleeve.', 1299, 25),
    ('USB-C Hub', '7-in-1 hub: HDMI, USB 3.0, SD card reader and PD charging.', 1799, 20),
    ('Portable Speaker', 'Pocket-size speaker with deep bass and 12-hour playtime.', 1999, 12),
]


class Command(BaseCommand):
    help = 'Add sample products to the store'

    def handle(self, *args, **options):
        for name, desc, price, stock in SAMPLE:
            Product.objects.get_or_create(
                name=name,
                defaults={'description': desc, 'price': price, 'stock': stock,
                          'image_url': f'https://picsum.photos/seed/{name.replace(" ", "")}/400/300'},
            )
        self.stdout.write(self.style.SUCCESS('Sample products added.'))
