# app/management/commands/import_products.py
import csv
from django.core.management.base import BaseCommand
from app.models import SanPham
import json

class Command(BaseCommand):
    help = 'Import sản phẩm từ file CSV'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Đường dẫn tới file CSV')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']
        
        # Hàm xử lý JSON an toàn
        def safe_json_loads(data):
            try:
                return json.loads(data) if data else {}
            except (json.JSONDecodeError, TypeError):
                return {}

        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                SanPham.objects.create(
                    main_category=row['main_category'],
                    title=row['title'],
                    average_rating=row['average_rating'] or None,
                    rating_number=row['rating_number'] or None,
                    features=safe_json_loads(row['features']),
                    description=safe_json_loads(row['description']),
                    price=row['price'] or None,
                    images=safe_json_loads(row['images']),
                    videos=safe_json_loads(row['videos']),
                    store=row['store'],
                    categories=safe_json_loads(row['categories']),
                    details=safe_json_loads(row['details']),
                    parent_asin=row['parent_asin'] or None,
                    bought_together=safe_json_loads(row['bought_together'])
                )
                self.stdout.write(f"Đã thêm sản phẩm: {row['title']}")
