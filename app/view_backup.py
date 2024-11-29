import os
import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.shortcuts import render
from django.http import HttpResponse

# Cấu hình NLTK và tải stopwords
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
stop_words = set(stopwords.words('english'))

# Cấu hình đường dẫn
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'app\code_hkmay', 'sentiment_model.pkl')
VECTORIZER_PATH = os.path.join(BASE_DIR, 'app\code_hkmay', 'vectorizer.pkl')


# Hàm tiền xử lý văn bản
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())  # Loại bỏ ký tự không phải chữ cái
    words = word_tokenize(text)  # Tách từ
    words = [word for word in words if word not in stop_words]  # Loại bỏ stopwords
    return ' '.join(words)


# Tải mô hình và vectorizer
try:
    with open(MODEL_PATH, 'rb') as model_file:
        model = pickle.load(model_file)

    with open(VECTORIZER_PATH, 'rb') as vectorizer_file:
        tfidf = pickle.load(vectorizer_file)
except FileNotFoundError as e:
    model, tfidf = None, None
    print(f"Lỗi: {e}")


# # Hàm dự đoán cảm xúc
# def predict_sentiment(new_text):
#     if not model or not tfidf:
#         return "Lỗi: Không thể tải mô hình hoặc vectorizer."
#
#     # Tiền xử lý câu mới
#     processed_text = preprocess_text(new_text)
#
#     # Vector hóa câu mới
#     new_text_tfidf = tfidf.transform([processed_text])
#
#     # Dự đoán cảm xúc
#     predicted_sentiment = model.predict(new_text_tfidf)[0]
#     return "Tich cuc" if predicted_sentiment == 1 else "Tieu cuc"
def predict_sentiment(new_text):
    if not model or not tfidf:
        return "Lỗi: Không thể tải mô hình hoặc vectorizer."
    # Tiền xử lý câu mới
    processed_text = preprocess_text(new_text)

    # Vector hóa câu mới
    new_text_tfidf = tfidf.transform([processed_text])  # Chuyển câu thành dạng vector

    # Dự đoán cảm xúc
    predicted_sentiment = model.predict(new_text_tfidf)
    return predicted_sentiment[0]

# Trang chủ
def home(request):
    return render(request, 'app/home.html')


# Trang dự đoán cảm xúc
def test_text(request):
    context = {}
    if request.method == 'POST':
        input_text = request.POST.get('text_camxuc', '').strip()  # Lấy dữ liệu từ form
        if input_text:
            result = predict_sentiment(input_text)  # Dự đoán cảm xúc
            context['NoiDung']=f"Văn bản :{input_text}"
            context['result'] = f"Kết quả dự đoán: {result}"
        else:
            context['result'] = "Vui lòng nhập văn bản."
    return render(request, 'app/test_text.html', context)
print("MODEL_PATH:", MODEL_PATH)
print("VECTORIZER_PATH:", VECTORIZER_PATH)


