import streamlit as st
from textblob import TextBlob
from langdetect import detect, DetectorFactory

# Чтобы результаты были стабильными
DetectorFactory.seed = 0

st.set_page_config(page_title="Linguistic Analyzer", page_icon="📝")

st.title("Linguistic & Sentiment Analyzer")
st.write("Upload your essay or paste text below to analyze its complexity and tone.")

# Поле для ввода
user_text = st.text_area("Enter your text here:", height=200)

if st.button("Analyze Text"):
    if user_text:
        # 1. Определяем язык
        try:
            lang = detect(user_text)
        except:
            lang = "unknown"
        
        # 2. Базовые метрики (работают для всех языков)
        word_count = len(user_text.split())
        st.subheader("General Metrics")
        col1, col2 = st.columns(2)
        col1.metric("Word Count", word_count)
        col2.metric("Detected Language", lang.upper())

        # 3. Глубокий анализ для английского
        if lang == 'en':
            blob = TextBlob(user_text)
            
            st.subheader("Advanced English Analysis")
            
            # Оценка тональности (Sentiment)
            sentiment = blob.sentiment.polarity
            if sentiment > 0.1:
                st.info("Tone: Positive. This is great for motivational letters!")
            elif sentiment < -0.1:
                st.warning("Tone: Negative/Critical. Ensure this is intentional for your essay.")
            else:
                st.secondary("Tone: Neutral/Objective.")


            # Сложность лексики (уникальные слова)
            unique_words = len(set(blob.words.lower()))
            lexical_richness = (unique_words / word_count) * 100 if word_count > 0 else 0
            st.write(f"**Lexical Richness:** {lexical_richness:.1f}% unique words.")
            
            if lexical_richness < 40:
                st.error("Tip: Try to use more diverse vocabulary to avoid repetition.")
            else:
                st.success("Tip: Your vocabulary variety looks solid!")

        else:
            st.warning("Detailed linguistic analysis (Sentiment/Complexity) is currently only available for English. For other languages, we only provide word counts.")
    else:
        st.error("Please enter some text first!")
