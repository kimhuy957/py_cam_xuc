from django.contrib import admin
from .models import *

# Đăng ký mô hình SanPham vào admin
@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    # Các trường hiển thị trong danh sách
    list_display = ('title', 'main_category', 'price', 'average_rating', 'store')
    
    # Các trường có thể tìm kiếm trong admin
    search_fields = ('title', 'main_category', 'store')
    
    # Các bộ lọc để phân loại trong admin
    list_filter = ('main_category', 'store')
    
    # Các trường có thể chỉnh sửa trực tiếp từ danh sách
    list_editable = ('price',)
    
    # Hiển thị chi tiết hơn trong mỗi bản ghi
    fields = ('title', 'main_category', 'price', 'average_rating', 'store', 'description', 'features')
    
    # Trường chỉ đọc trong chi tiết khi chỉnh sửa đối tượng
    readonly_fields = ('average_rating',)

# Đăng ký mô hình Comment vào admin
@admin.register(ProductReview)
class CommentAdmin(admin.ModelAdmin):
    # Các trường hiển thị trong danh sách
    list_display = ('title', 'asin', 'user_id', 'rating', 'timestamp', 'sentiment')
    
    # Các trường có thể tìm kiếm trong admin
    search_fields = ('title', 'asin', 'user_id')
    
    # Các bộ lọc để phân loại trong admin
    list_filter = ('sentiment', 'verified_purchase')
    
    # Các trường có thể chỉnh sửa trực tiếp từ danh sách
    list_editable = ('sentiment',)
    
    # Hiển thị chi tiết hơn trong mỗi bản ghi
    fields = ('title', 'asin', 'user_id', 'rating', 'text', 'images', 'verified_purchase', 'sentiment', 'processed_text')
    

