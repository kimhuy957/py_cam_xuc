import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer  # Sử dụng CountVectorizer thay vì TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import re
import logging
import pickle

# Cấu hình logging
logging.basicConfig(
    filename='ketqua_log.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Tải các tài nguyên cần thiết cho NLTK
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)

# Xác định stopwords
stop_words = set(stopwords.words('english'))

# Hàm tiền xử lý văn bản
def preprocess_text(text):
    text = re.sub(r'[^a-zA-Z\s]', ' ', text.lower())  # Loại bỏ ký tự không phải chữ cái
    words = word_tokenize(text)  # Tách từ
    words = [word for word in words if word not in stop_words and len(word) > 1]  # Loại bỏ stopwords
    return ' '.join(words)

# Đọc file CSV
file_path = r'All_Beauty.csv'  # Thay bằng đường dẫn file của bạn
try:
    logging.info(f"Đang xử lý file: {file_path}")
    # Thử với mã hóa mặc định và mã hóa fallback nếu gặp lỗi
    try:
        df = pd.read_csv(file_path, encoding='latin1')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
except Exception as e:
    logging.error(f"Lỗi khi đọc file CSV: {e}")
    raise SystemExit(f"Lỗi khi đọc file CSV: {e}")

# Kiểm tra và làm sạch dữ liệu
if 'text' not in df.columns or 'sentiment' not in df.columns:
    raise KeyError("File CSV cần chứa cột 'text' và 'sentiment'.")
df.dropna(subset=['text', 'sentiment'], inplace=True)  # Loại bỏ hàng không có dữ liệu

# Tiền xử lý văn bản
df['processed_text'] = df['text'].apply(preprocess_text)

# Chia dữ liệu thành tập huấn luyện, kiểm tra và xác nhận
X_train, X_temp, y_train, y_temp = train_test_split(df['processed_text'], df['sentiment'], test_size=0.2, random_state=42)
X_test, X_val, y_test, y_val = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)

# Vector hóa dữ liệu bằng BoW (CountVectorizer)
vectorizer = CountVectorizer(max_features=1000)  # Sử dụng CountVectorizer thay vì TfidfVectorizer
X_train_bow = vectorizer.fit_transform(X_train)
X_test_bow = vectorizer.transform(X_test)
X_val_bow = vectorizer.transform(X_val)

# Huấn luyện mô hình Naive Bayes
model = MultinomialNB()
model.fit(X_train_bow, y_train)

# Đánh giá mô hình trên tập kiểm tra
y_pred_test = model.predict(X_test_bow)
accuracy_test = accuracy_score(y_test, y_pred_test)
logging.info(f"Độ chính xác trên tập kiểm tra: {accuracy_test}")
logging.info("Classification Report trên tập kiểm tra:\n" + classification_report(y_test, y_pred_test))

print("Độ chính xác trên tập kiểm tra:", accuracy_test)
print("Classification Report trên tập kiểm tra:\n", classification_report(y_test, y_pred_test))

# Đánh giá mô hình trên tập xác nhận
y_pred_val = model.predict(X_val_bow)
accuracy_val = accuracy_score(y_val, y_pred_val)
logging.info(f"Độ chính xác trên tập xác nhận: {accuracy_val}")
print("Độ chính xác trên tập xác nhận:", accuracy_val)

# Lưu kết quả ra file mới
output_file = file_path.split('\\')[-1].replace('.csv', '_ket_qua2.csv')
df['predicted_sentiment'] = model.predict(vectorizer.transform(df['processed_text']))
df.to_csv(output_file, index=False)
logging.info(f"Kết quả được lưu vào: {output_file}")
print(f"Kết quả được lưu vào: {output_file}")

# Lưu mô hình Naive Bayes và vectorizer (BoW) để sử dụng lại sau này
with open('sentiment_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Mô hình và vectorizer đã được lưu.")
