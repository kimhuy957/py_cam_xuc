import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from app.models import ProductReview


class Command(BaseCommand):
    help = 'Import reviews from CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file_path']

        # Đọc file CSV
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            # Lặp qua từng dòng trong CSV và tạo đối tượng ProductReview
            for row in reader:
                # Kiểm tra và chuyển đổi timestamp sang định dạng DD/MM/YYYY HH:MM:SS
                try:
                    # Kiểm tra xem timestamp có phải là số hợp lệ không
                    timestamp = int(row['timestamp'])

                    # Kiểm tra xem timestamp có nằm trong khoảng hợp lệ không
                    if timestamp < 0 or timestamp > 3250368000000:  # Kiểm tra với giá trị lớn hợp lý (năm 3000, tính bằng milliseconds)
                        raise ValueError(f"Invalid timestamp value: {timestamp}")

                    # Chuyển đổi timestamp Unix từ milliseconds sang giây
                    timestamp_s = timestamp / 1000
                    dt = datetime.utcfromtimestamp(timestamp_s)

                    # Kiểm tra nếu năm nhỏ hơn 2022, thay đổi năm thành 2023
                    if dt.year < 2022:
                        dt = dt.replace(year=2023)

                    # Chuyển đổi datetime thành định dạng chuỗi
                    formatted_timestamp = dt.strftime('%d/%m/%Y %H:%M:%S')
                except (ValueError, KeyError) as e:  # Nếu không có timestamp hoặc lỗi chuyển đổi
                    self.stderr.write(f"Error processing row {row['asin']}: {e}")
                    formatted_timestamp = None  # Hoặc có thể gán giá trị mặc định khác

                # Tạo mới đối tượng ProductReview và lưu vào DB
                ProductReview.objects.create(
                    rating=float(row['rating']),
                    title=row['title'],
                    text=row['text'],
                    images=row['images'],
                    asin=row['asin'],
                    parent_asin=row['parent_asin'] or None,
                    user_id=row['user_id'],
                    timestamp=formatted_timestamp,  # Sử dụng timestamp đã được định dạng
                    helpful_vote=int(row['helpful_vote']),
                    verified_purchase=row['verified_purchase'].lower() == 'true',  # Chuyển thành boolean
                    processed_text=row['processed_text'],
                    sentiment=row['sentiment'],
                    predicted_sentiment=row['predicted_sentiment']
                )

                # In ra thông báo với màu đỏ
                self.stdout.write(f"\033[91m Đã có lỗi hàng : {row['title']}\033[0m")
