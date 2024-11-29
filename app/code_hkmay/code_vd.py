import pickle
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Cấu hình NLTK và tải stopwords
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
stop_words = set(stopwords.words('english'))


# Hàm tiền xử lý văn bản
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', text.lower())  # Loại bỏ ký tự không phải chữ cái
    words = word_tokenize(text)  # Tách từ
    words = [word for word in words if word not in stop_words]  # Loại bỏ stopwords
    return ' '.join(words)


# Tải mô hình và vectorizer đã lưu
with open('sentiment_model.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

with open('vectorizer.pkl', 'rb') as vectorizer_file:
    tfidf = pickle.load(vectorizer_file)


# Dự đoán cảm xúc cho câu mới
def predict_sentiment(new_text):
    # Tiền xử lý câu mới
    processed_text = preprocess_text(new_text)

    # Vector hóa câu mới
    new_text_tfidf = tfidf.transform([processed_text])  # Chuyển câu thành dạng vector

    # Dự đoán cảm xúc
    predicted_sentiment = model.predict(new_text_tfidf)
    return predicted_sentiment[0]


# Ví dụ sử dụng: dự đoán cảm xúc cho câu mới
new_text = "I hated it. The product was nothing like described"  # Câu mới cần dự đoán
predicted_sentiment = predict_sentiment(new_text)
print(f"Câu: {new_text}")
print(f"Dự đoán cảm xúc: {predicted_sentiment}")
