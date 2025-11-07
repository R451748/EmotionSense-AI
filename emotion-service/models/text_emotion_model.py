import os
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras import mixed_precision

# ================================================
# ⚙️ GPU & Mixed Precision Setup

# ================================================
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"✅ GPU detected: {gpus[0].name}")
    except RuntimeError as e:
        print(e)
else:
    print("⚠️ No GPU detected. Running on CPU.")

mixed_precision.set_global_policy('mixed_float16')
print("🚀 Mixed precision enabled for faster GPU training!")

# ================================================
# 📂 Dataset Paths
# ================================================
BASE_PATH = r"C:\Users\rohan\Desktop\EmotionSense\emotion-service\datasets\text\emotions-dataset-for-nlp"
TRAIN_FILE = os.path.join(BASE_PATH, "train.txt")
TEST_FILE = os.path.join(BASE_PATH, "test.txt")
VAL_FILE = os.path.join(BASE_PATH, "val.txt")

# ================================================
# 🧠 Load & Prepare Data
# ================================================
def load_data():
    train_df = pd.read_csv(TRAIN_FILE, sep=';', header=None, names=['text', 'emotion'])
    test_df = pd.read_csv(TEST_FILE, sep=';', header=None, names=['text', 'emotion'])
    val_df = pd.read_csv(VAL_FILE, sep=';', header=None, names=['text', 'emotion'])
    df = pd.concat([train_df, test_df, val_df], ignore_index=True)
    print(f"📊 Loaded {len(df)} samples across {df['emotion'].nunique()} emotions.")
    return df

# ================================================
# 🧩 Tokenization & Padding
# ================================================
def preprocess_text(df):
    tokenizer = Tokenizer(num_words=20000, oov_token="<OOV>")
    tokenizer.fit_on_texts(df['text'])
    sequences = tokenizer.texts_to_sequences(df['text'])
    padded = pad_sequences(sequences, maxlen=120, truncating='post', padding='post')

    label_tokenizer = Tokenizer()
    label_tokenizer.fit_on_texts(df['emotion'])
    labels = np.array([label_tokenizer.texts_to_sequences([e])[0][0] - 1 for e in df['emotion']])

    return tokenizer, label_tokenizer, padded, labels

# ================================================
# 🧠 Load Pretrained GloVe Embeddings
# ================================================
def load_glove_embeddings(tokenizer, embedding_dim=100):
    glove_path = r"C:\Users\rohan\Desktop\EmotionSense\emotion-service\datasets\glove.6B\glove.6B.100d.txt"
    print("📥 Loading GloVe embeddings (100D)...")

    embeddings_index = {}
    with open(glove_path, encoding='utf8') as f:
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs

    embedding_matrix = np.zeros((20000, embedding_dim))
    for word, i in tokenizer.word_index.items():
        if i < 20000:
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector

    print(f"✅ Loaded {len(embeddings_index)} word vectors from GloVe.")
    return embedding_matrix

# ================================================
# 🏗️ Build Model
# ================================================
def build_model(num_classes, embedding_matrix):
    model = Sequential([
        Embedding(20000, 100, weights=[embedding_matrix], input_length=120, trainable=False),
        Bidirectional(LSTM(128, dropout=0.4, recurrent_dropout=0.4)),
        Dense(128, activation='relu'),
        Dropout(0.5),
        Dense(num_classes, activation='softmax')
    ])
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.summary()
    return model

# ================================================
# 🚀 Train Model
# ================================================
def train_text_model():
    df = load_data()
    tokenizer, label_tokenizer, padded, labels = preprocess_text(df)
    embedding_matrix = load_glove_embeddings(tokenizer)
    num_classes = len(label_tokenizer.word_index)

    model = build_model(num_classes, embedding_matrix)

    # ✅ Callbacks for better generalization
    early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=2)

    print("\n🚀 Starting Training...\n")
    history = model.fit(
        padded, labels,
        epochs=25,
        validation_split=0.2,
        batch_size=64,
        callbacks=[early_stop, lr_scheduler],
        verbose=1
    )

    # ================================================
    # 💾 Save Model & Tokenizers
    # ================================================
    model_dir = r"C:\Users\rohan\Desktop\EmotionSense\emotion-service\models"
    os.makedirs(model_dir, exist_ok=True)

    model.save(os.path.join(model_dir, "text_emotion_model_v2.h5"))
    with open(os.path.join(model_dir, "text_tokenizer.pkl"), "wb") as f:
        pickle.dump(tokenizer, f)
    with open(os.path.join(model_dir, "label_tokenizer.pkl"), "wb") as f:
        pickle.dump(label_tokenizer, f)

    print("\n✅ Model & Tokenizers Saved Successfully!")
    print("📈 Final Accuracy:", round(max(history.history['val_accuracy']) * 100, 2), "%")

# ================================================
# ▶️ Run
# ================================================
if __name__ == "__main__":
    train_text_model()
