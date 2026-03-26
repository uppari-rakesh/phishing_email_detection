import pandas as pd
import re
import string
import pickle

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.ensemble import RandomForestClassifier
from scipy.sparse import hstack
import nltk

# Download stopwords (first time only)
nltk.download("stopwords")

# -------------------------
# LOAD DATA
# -------------------------
df = pd.read_csv("data/Nigerian_Fraud.csv")

# Check columns
print("Columns:", df.columns)

# -------------------------
# TEXT CLEANING
# -------------------------
stop_words = set(stopwords.words("english"))
stemmer = PorterStemmer()

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", " url ", text)
    text = re.sub(r"\S+@\S+", " email ", text)
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " number ", text)
    return " ".join(
        stemmer.stem(word) for word in text.split() if word not in stop_words
    )

df["clean_text"] = df["text"].apply(clean_text)

# -------------------------
# FEATURE ENGINEERING
# -------------------------
df["url_count"] = df["text"].apply(lambda x: str(x).count("http"))
df["email_length"] = df["text"].apply(lambda x: len(str(x)))

suspicious_words = ["verify", "urgent", "login", "bank", "click", "password"]
df["suspicious_count"] = df["text"].apply(
    lambda x: sum(word in str(x).lower() for word in suspicious_words)
)

df["uppercase_count"] = df["text"].apply(
    lambda x: sum(1 for c in str(x) if c.isupper())
)

df["special_char_count"] = df["text"].apply(
    lambda x: sum(1 for c in str(x) if not c.isalnum())
)

# -------------------------
# TF-IDF
# -------------------------
tfidf = TfidfVectorizer(max_features=3000)
X_text = tfidf.fit_transform(df["clean_text"])

# Combine meta features
X_meta = df[[
    "email_length",
    "url_count"
]]

# Combine all features
X = hstack([X_text, X_meta])

# Labels
y = df["spam"]

# -------------------------
# TRAIN TEST SPLIT
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -------------------------
# MODEL TRAINING
# -------------------------
model = RandomForestClassifier(class_weight="balanced")

# Hyperparameter tuning
params = {
    "n_estimators": [100, 200],
    "max_depth": [None, 10, 20]
}

grid = GridSearchCV(
    model,
    params,
    cv=3,
    scoring="f1",
    n_jobs=-1
)

grid.fit(X_train, y_train)

best_model = grid.best_estimator_

print("\nBest Parameters:", grid.best_params_)

# -------------------------
# EVALUATION
# -------------------------
y_pred = best_model.predict(X_test)
y_prob = best_model.predict_proba(X_test)[:, 1]

print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

print("ROC-AUC Score:", roc_auc_score(y_test, y_prob))

# -------------------------
# SAVE MODEL
# -------------------------
import os

# create model folder if not exists
if not os.path.exists("model"):
    os.makedirs("model")

pickle.dump(best_model, open("model/phishing_model.pkl", "wb"))
pickle.dump(tfidf, open("model/tfidf.pkl", "wb"))

print("\n✅ MODEL SAVED SUCCESSFULLY")