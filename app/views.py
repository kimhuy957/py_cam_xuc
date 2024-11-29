# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# import pickle
# import re
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# import nltk
# import os
# # import pickle
# # Tải stopwords và cấu hình NLTK
# nltk.download('stopwords', quiet=True)
# nltk.download('punkt', quiet=True)
# stop_words = set(stopwords.words('english'))
#
# # Hàm tiền xử lý văn bản
# def preprocess_text(text):
#     text = re.sub(r'[^a-zA-Z\s]', '', text.lower())  # Loại bỏ ký tự không phải chữ cái
#     words = word_tokenize(text)  # Tách từ
#     words = [word for word in words if word not in stop_words]  # Loại bỏ stopwords
#     return ' '.join(words)
#
# # Đường dẫn tuyệt đối đến tệp
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Thư mục hiện tại
# MODEL_PATH = os.path.join(BASE_DIR, 'code_hkmay', 'sentiment_model.pkl')
# VECTORIZER_PATH = os.path.join(BASE_DIR, 'code_hkmay', 'vectorizer.pkl')
#
# # Kiểm tra và tải mô hình, vectorizer
# if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
#     with open(MODEL_PATH, 'rb') as model_file:
#         model = pickle.load(model_file)
#     with open(VECTORIZER_PATH, 'rb') as vectorizer_file:
#         tfidf = pickle.load(vectorizer_file)
# else:
#     raise FileNotFoundError("Không thể tìm thấy các file cần thiết (model/vectorizer).")
#
# # View dự đoán cảm xúc
# def predict_sentiment(request):
#     result = None
#     NoiDung = None
#     if request.method == 'POST':
#         user_input = request.POST.get('text_camxuc')  # Lấy nội dung người dùng nhập
#         NoiDung = user_input
#         processed_text = preprocess_text(user_input)  # Tiền xử lý văn bản
#         text_vector = tfidf.transform([processed_text])  # Chuyển văn bản thành vector
#         result = model.predict(text_vector)[0]  # Dự đoán cảm xúc
#     return render(request, 'app/predict_sentiment.html', {'result': result, 'NoiDung': NoiDung})
#
# # View lưu cảm xúc "Like"
# def save_sentiment(request):
#     if request.method == "POST":
#         processed_text = request.POST.get("processed_text")
#         sentiment = request.POST.get("sentiment")
#
#         if sentiment == "like":
#             with open('training_data.csv', 'a') as f:
#                 f.write(f"{processed_text},like\n")
#             return HttpResponse("Cảm xúc đã được lưu thành công!")
#     return redirect('predict_sentiment')
#
# # View bỏ qua cảm xúc "No Like"
# def discard_sentiment(request):
#     return HttpResponse("Cảm xúc không được lưu và đã bỏ qua.")


from django.shortcuts import render
from django.http import JsonResponse
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os
from django.shortcuts import redirect
# from django.http import JsonResponse

# Tải tài nguyên NLTK cần thiết
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
stop_words = set(stopwords.words('english'))
# Đường dẫn tuyệt đối đến tệp
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Thư mục hiện tại
MODEL_PATH = os.path.join(BASE_DIR, 'code_hkmay', 'sentiment_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'code_hkmay', 'vectorizer.pkl')

# Kiểm tra và tải mô hình, vectorizer
if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(VECTORIZER_PATH, 'rb') as vectorizer_file:
        tfidf = pickle.load(vectorizer_file)
else:
    raise FileNotFoundError("Không thể tìm thấy các file cần thiết (model/vectorizer).")


# Hàm xử lý văn bản
def preprocess_text(text):
    """Tiền xử lý văn bản: loại bỏ ký tự không cần thiết, xóa stopwords."""
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())  # Chuyển về chữ thường, loại bỏ ký tự đặc biệt
    words = word_tokenize(text)  # Tách từ
    words = [word for word in words if word not in stop_words]  # Loại bỏ stopwords
    return ' '.join(words)


# Trang chính
def home(request):
    """Hiển thị trang chính."""
    return render(request, 'app/home.html')


# Hàm xử lý dự đoán cảm xúc
def test_text(request):
    """Dự đoán cảm xúc từ văn bản nhập vào."""
    result = None
    NoiDung = None
    if request.method == 'POST':
        # Lấy dữ liệu từ người dùng
        text_input = request.POST.get('text_camxuc', '')

        if text_input:
            # Tiền xử lý văn bản
            processed_text = preprocess_text(text_input)

            # Vector hóa văn bản
            text_tfidf = tfidf.transform([processed_text])

            # Dự đoán cảm xúc
            predicted_sentiment = model.predict(text_tfidf)
            NoiDung = text_input

            result = 'Tích cực 😊' if predicted_sentiment[0] == 'Tich cuc' else 'Tiêu cực 😞'

    # Render kết quả
    return render(request, 'app/test_text.html', {'result': result, 'NoiDung': NoiDung})


def save_sentiment(request):
    """Lưu lại văn bản tích cực vào mô hình."""
    if request.method == 'POST':
        text_input = request.POST.get('text')
        if text_input:
            # Tiền xử lý và lưu
            processed_text = preprocess_text(text_input)
            with open('./code_hkmay/liked_texts.txt', 'a') as f:
                f.write(f"{processed_text}\n")
        print("Redirecting to /text")
        return redirect('text')  # Chuyển hướng về trang text

def discard_sentiment(request):
    """Bỏ qua văn bản tiêu cực, không lưu lại."""
    if request.method == 'POST':
        print("Redirecting to /text")
        return redirect('text')  # Chuyển hướng về trang text
