import streamlit as st
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import os

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def clean_text(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\d+', '', text)
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stop_words])
    return text.strip()

@st.cache_data
def load_and_prepare_data(true_path, fake_path):
    df_true = pd.read_csv(true_path)
    df_fake = pd.read_csv(fake_path)

    df_true['label'] = 1
    df_fake['label'] = 0

    df = pd.concat([df_true, df_fake], ignore_index=True)

    df.drop_duplicates(subset='text', inplace=True)
    df.dropna(subset=['text'], inplace=True)

    df['text'] = df['text'].apply(clean_text)
    return df

def train_and_evaluate(df, model_name):
    X = df['text']
    y = df['label']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # ✅ تقليل عدد الميزات لتسريع التدريب
    vectorizer = TfidfVectorizer(max_features=5000, min_df=5, max_df=0.8)
    X_train_vectorized = vectorizer.fit_transform(X_train)
    X_test_vectorized = vectorizer.transform(X_test)

    if model_name == "Naive Bayes":
        model = MultinomialNB()
    elif model_name == "Logistic Regression":
        model = LogisticRegression(max_iter=1000)
    elif model_name == "Random Forest":
        model = RandomForestClassifier()
    elif model_name == "SVM":
        # ✅ استبدال SVC بـ LinearSVC لتسريع التدريب
        model = LinearSVC()
    elif model_name == "XGBoost":
        model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    else:
        raise ValueError("Invalid model name")

    model.fit(X_train_vectorized, y_train)
    predictions = model.predict(X_test_vectorized)

    acc = accuracy_score(y_test, predictions)
    report = classification_report(y_test, predictions, output_dict=True)
    cm = confusion_matrix(y_test, predictions)

    # ✅ تقييم النموذج الحقيقي باستخدام Cross Validation
    cross_val_scores = cross_val_score(model, X_train_vectorized, y_train, cv=5, scoring='accuracy')
    avg_cv = np.mean(cross_val_scores)

    return vectorizer, model, acc, report, cm, avg_cv

def plot_all_together(df, report, cm):
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    counts = df['label'].value_counts()
    labels = ['True', 'Fake']
    axes[0, 0].pie(counts, labels=labels, autopct='%1.1f%%', colors=['#2ecc71', '#e74c3c'])
    axes[0, 0].set_title("News Distribution")

    all_words = ' '.join(df['text']).split()
    common_words = Counter(all_words).most_common(15)
    words, freqs = zip(*common_words)
    sns.barplot(x=list(words), y=list(freqs), ax=axes[0, 1], palette="viridis")
    axes[0, 1].set_title("Top 15 Most Common Words")
    axes[0, 1].tick_params(axis='x', rotation=45)

    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=axes[1, 0],
                xticklabels=["Fake", "True"], yticklabels=["Fake", "True"])
    axes[1, 0].set_title("Confusion Matrix")
    axes[1, 0].set_xlabel("Predicted")
    axes[1, 0].set_ylabel("Actual")

    metrics = ['precision', 'recall', 'f1-score']
    scores = [report['1'][m] for m in metrics]
    sns.barplot(x=metrics, y=scores, ax=axes[1, 1], palette="Set2")
    axes[1, 1].set_title("Model Performance (True News)")
    axes[1, 1].set_ylim(0, 1)

    plt.tight_layout()
    st.pyplot(fig)

def main():
    st.set_page_config(page_title="News Classification App", layout="wide")
    st.title("📰 Fake News Detection Using NLP")

    true_data_path = r'C:\Users\PROCESSOR\Desktop\NLP\True.csv'
    fake_data_path = r'C:\Users\PROCESSOR\Desktop\NLP\Fake.csv'

    if not os.path.exists(true_data_path) or not os.path.exists(fake_data_path):
        st.error("Make sure True.csv and Fake.csv files exist in the specified path.")
        return

    with st.spinner("Loading data and preparing..."):
        dataframe = load_and_prepare_data(true_data_path, fake_data_path)

    st.sidebar.title("⚙️ Model Settings")
    model_choice = st.sidebar.selectbox("Choose a model:", [
        "Naive Bayes", "Logistic Regression", "Random Forest", "SVM", "XGBoost"
    ])

    with st.spinner("Training and evaluating..."):
        vectorizer, model, acc, report, cm, avg_cv = train_and_evaluate(dataframe, model_choice)

    st.success("✅ Model trained and evaluated!")
    st.markdown(f"**Selected Model:** `{model_choice}`")
    st.markdown(f"**Test Set Accuracy:** `{acc * 100:.2f}%`")
    st.markdown(f"**Average Cross-Validation Accuracy (5-Fold):** `{avg_cv * 100:.2f}%`")

    st.subheader("📊 Data Analysis & Evaluation")
    plot_all_together(dataframe, report, cm)

    st.subheader("📝 Try the Model")
    user_input = st.text_area("Enter your news text:")
    if st.button("Classify"):
        if user_input.strip():
            cleaned_input = clean_text(user_input)
            vectorized_input = vectorizer.transform([cleaned_input])
            prediction = model.predict(vectorized_input)[0]
            label = "✅ Real News" if prediction == 1 else "❌ Fake News"
            st.success(f"Prediction: {label}")
        else:
            st.warning("Please enter some news text.")

if __name__ == "__main__":
    main()
