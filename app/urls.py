from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    # Đường dẫn chính đến trang chủ
    path('', views.home, name="home"),

    # Đường dẫn đến tính năng kiểm tra cảm xúc từ văn bản
    path('text', views.test_text, name="text"),

    # Đường dẫn để lưu cảm xúc (Like)
    path('save_sentiment/', views.save_sentiment, name='save_sentiment'),

    # Đường dẫn để bỏ qua cảm xúc (No Like)
    path('discard_sentiment/', views.discard_sentiment, name='discard_sentiment'),
]
