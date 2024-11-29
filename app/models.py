from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class SanPham(models.Model):
    main_category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    rating_number = models.FloatField(null=True, blank=True)
    features = models.JSONField(blank=True, null=True)  # Sử dụng JSONField để lưu trữ danh sách
    description = models.JSONField(blank=True, null=True)  # Sử dụng JSONField để lưu trữ danh sách
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Có thể null
    images = models.JSONField(blank=True, null=True)  # Sử dụng JSONField để lưu trữ danh sách ảnh
    videos = models.JSONField(blank=True, null=True)  # Sử dụng JSONField để lưu trữ danh sách video
    store = models.CharField(max_length=100)
    categories = models.JSONField(blank=True, null=True)  # Sử dụng JSONField để lưu trữ danh sách
    details = models.JSONField(blank=True, null=True)  # Sử dụng JSONField để lưu trữ thông tin chi tiết
    parent_asin = models.CharField(max_length=10, null=True, blank=True)
    bought_together = models.JSONField(blank=True, null=True)  # Sử dụng JSONField nếu có

    def __str__(self):
        return self.title
    
class ProductReview(models.Model):
    rating = models.FloatField()  # Điểm đánh giá
    title = models.CharField(max_length=255)  # Tiêu đề đánh giá
    text = models.TextField()  # Nội dung đánh giá
    images = models.TextField()  # Đường dẫn hoặc URL của hình ảnh liên quan đến đánh giá
    asin = models.CharField(max_length=50)  # ASIN của sản phẩm
    parent_asin = models.CharField(max_length=50, blank=True, null=True)  # ASIN của sản phẩm cha
    user_id = models.CharField(max_length=100)  # ID của người dùng
    timestamp = models.DateTimeField(auto_now_add=True)  # Thời gian đánh giá
    helpful_vote = models.IntegerField()  # Số phiếu hữu ích
    verified_purchase = models.BooleanField()  # Đánh giá đã được xác thực là đã mua
    processed_text = models.TextField()  # Văn bản đã xử lý
    sentiment = models.CharField(max_length=20)  # Cảm xúc (Positive, Negative, Neutral)
    predicted_sentiment = models.CharField(max_length=20)  # Cảm xúc dự đoán


    def __str__(self):
        return self.title  # Trả về tiêu đề đánh giá khi gọi tên đối tượng
