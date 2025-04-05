from django.core.management.base import BaseCommand
from base.models import Category

class Command(BaseCommand):
    help = 'Creates initial categories for the Binary Hub marketplace'

    def handle(self, *args, **kwargs):
        categories = [
            {
                'name': 'Metal',
                'description': 'Metal scraps including aluminum, steel, copper, and more.'
            },
            {
                'name': 'Paper',
                'description': 'Paper and cardboard materials for recycling and reuse.'
            },
            {
                'name': 'Plastic',
                'description': 'Various plastic items and materials that can be recycled or repurposed.'
            },
            {
                'name': 'Electronics',
                'description': 'Electronic components, devices, and parts for reuse or recycling.'
            },
            {
                'name': 'Glass',
                'description': 'Glass bottles, jars, and other glass materials.'
            },
            {
                'name': 'Wood',
                'description': 'Wood scraps, lumber, and wooden items for repurposing.'
            },
            {
                'name': 'Textile',
                'description': 'Fabric, clothing, and other textile materials.'
            },
            {
                'name': 'Construction',
                'description': 'Building materials and construction waste that can be reused.'
            },
        ]

        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category "{category.name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{category.name}" already exists'))

        self.stdout.write(self.style.SUCCESS('Initial categories have been created successfully.'))