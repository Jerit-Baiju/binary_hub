from django.core.management.base import BaseCommand
from base.models import Category, ScrapItem, Order
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Creates initial categories, users, products, and orders for the Binary Hub marketplace'

    def handle(self, *args, **kwargs):
        # Create categories
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

        created_categories = []
        for category_data in categories:
            category, created = Category.objects.get_or_create(
                name=category_data['name'],
                defaults={'description': category_data['description']}
            )
            created_categories.append(category)
            
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category "{category.name}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Category "{category.name}" already exists'))

        # Create dummy users
        self.create_users()
        
        # Create dummy scrap items
        self.create_scrap_items(created_categories)
        
        # Create dummy orders
        self.create_orders()

        self.stdout.write(self.style.SUCCESS('Initial data has been created successfully.'))
    
    def create_users(self):
        # Create dummy users (5 users)
        users_data = [
            {'username': 'johndoe', 'email': 'john@example.com', 'password': 'password123', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'janedoe', 'email': 'jane@example.com', 'password': 'password123', 'first_name': 'Jane', 'last_name': 'Doe'},
            {'username': 'mikebrown', 'email': 'mike@example.com', 'password': 'password123', 'first_name': 'Mike', 'last_name': 'Brown'},
            {'username': 'sarahsmith', 'email': 'sarah@example.com', 'password': 'password123', 'first_name': 'Sarah', 'last_name': 'Smith'},
            {'username': 'chrislee', 'email': 'chris@example.com', 'password': 'password123', 'first_name': 'Chris', 'last_name': 'Lee'},
        ]
        
        created_users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={
                    'email': user_data['email'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                created_users.append(user)
                self.stdout.write(self.style.SUCCESS(f'Created user "{user.username}"'))
            else:
                self.stdout.write(self.style.WARNING(f'User "{user.username}" already exists'))
                created_users.append(user)
        
        return created_users
    
    def create_scrap_items(self, categories):
        # Get all users
        users = User.objects.all()
        if not users:
            self.stdout.write(self.style.WARNING('No users found to create scrap items'))
            return
            
        # Create dummy scrap items (15 items)
        conditions = ['New', 'Like New', 'Good', 'Used', 'For parts']
        locations = ['New York', 'San Francisco', 'Chicago', 'Miami', 'Seattle', 'Boston', 'Dallas']
        
        scrap_items_data = [
            {'title': 'Copper Wire Bundle', 'price': '45.99', 'category_name': 'Metal', 'condition': 'Good', 'quantity': 3},
            {'title': 'Aluminum Scrap', 'price': '25.50', 'category_name': 'Metal', 'condition': 'Used', 'quantity': 5},
            {'title': 'Cardboard Boxes', 'price': '12.99', 'category_name': 'Paper', 'condition': 'Good', 'quantity': 10},
            {'title': 'Old Magazines', 'price': '8.75', 'category_name': 'Paper', 'condition': 'Used', 'quantity': 20},
            {'title': 'PVC Pipe Sections', 'price': '18.50', 'category_name': 'Plastic', 'condition': 'For parts', 'quantity': 8},
            {'title': 'Plastic Containers', 'price': '9.99', 'category_name': 'Plastic', 'condition': 'Good', 'quantity': 15},
            {'title': 'Computer Motherboard', 'price': '35.00', 'category_name': 'Electronics', 'condition': 'For parts', 'quantity': 1},
            {'title': 'LCD Screens', 'price': '42.75', 'category_name': 'Electronics', 'condition': 'Used', 'quantity': 2},
            {'title': 'Glass Bottles', 'price': '15.25', 'category_name': 'Glass', 'condition': 'Good', 'quantity': 12},
            {'title': 'Window Panes', 'price': '28.99', 'category_name': 'Glass', 'condition': 'Like New', 'quantity': 4},
            {'title': 'Wooden Pallets', 'price': '22.50', 'category_name': 'Wood', 'condition': 'Used', 'quantity': 6},
            {'title': 'Pine Lumber Offcuts', 'price': '19.75', 'category_name': 'Wood', 'condition': 'Good', 'quantity': 8},
            {'title': 'Denim Fabric Scraps', 'price': '14.50', 'category_name': 'Textile', 'condition': 'New', 'quantity': 7},
            {'title': 'Used Clothing Bulk', 'price': '32.99', 'category_name': 'Textile', 'condition': 'Good', 'quantity': 25},
            {'title': 'Concrete Blocks', 'price': '38.75', 'category_name': 'Construction', 'condition': 'Used', 'quantity': 10},
        ]
        
        created_items = []
        for item_data in scrap_items_data:
            # Find the category
            try:
                category = next(c for c in categories if c.name == item_data['category_name'])
            except StopIteration:
                self.stdout.write(self.style.WARNING(f'Category "{item_data["category_name"]}" not found, skipping item'))
                continue
            
            # Randomly assign a seller
            seller = random.choice(users)
            
            # Create the scrap item
            scrap_item, created = ScrapItem.objects.get_or_create(
                title=item_data['title'],
                seller=seller,
                defaults={
                    'description': f'This is a sample {item_data["title"]} for sale in the marketplace.',
                    'price': Decimal(item_data['price']),
                    'category': category,
                    'quantity': item_data['quantity'],
                    'location': random.choice(locations),
                    'condition': item_data['condition'],
                    'is_available': True,
                }
            )
            
            if created:
                created_items.append(scrap_item)
                self.stdout.write(self.style.SUCCESS(f'Created scrap item "{scrap_item.title}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Scrap item "{scrap_item.title}" already exists'))
                created_items.append(scrap_item)
        
        return created_items
    
    def create_orders(self):
        # Get all users and scrap items
        users = list(User.objects.all())
        if not users or len(users) < 2:
            self.stdout.write(self.style.WARNING('Not enough users found to create orders'))
            return
            
        scrap_items = list(ScrapItem.objects.all())
        if not scrap_items:
            self.stdout.write(self.style.WARNING('No scrap items found to create orders'))
            return
            
        # Create dummy orders (10 orders)
        statuses = ['pending', 'processing', 'shipped', 'delivered', 'canceled']
        
        for _ in range(10):
            # Select a random scrap item
            scrap_item = random.choice(scrap_items)
            
            # Make sure buyer and seller are different users
            seller = scrap_item.seller
            buyers = [user for user in users if user != seller]
            if not buyers:
                continue
            buyer = random.choice(buyers)
            
            # Random quantity between 1 and the available quantity
            quantity = random.randint(1, min(scrap_item.quantity, 3))
            
            # Calculate total price
            total_price = scrap_item.price * quantity
            
            # Create the order
            order = Order.objects.create(
                buyer=buyer,
                seller=seller,
                scrap_item=scrap_item,
                quantity=quantity,
                total_price=total_price,
                status=random.choice(statuses)
            )
            
            self.stdout.write(self.style.SUCCESS(f'Created order #{order.id} for "{scrap_item.title}"'))