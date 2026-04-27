import streamlit as st
from textblob import TextBlob
from langdetect import detect, DetectorFactory
import nltk

# Автоматическая загрузка необходимых компонентов при запуске
@st.cache_resource
def setup_nltk():
    nltk.download('punkt')
    nltk.download('punkt_tab')

setup_nltk()

# Для стабильности определения языка
DetectorFactory.seed = 0

st.set_page_config(page_title="Linguistic Analyzer", page_icon="📝")

st.title("Linguistic & Sentiment Analyzer")
st.write("Analyze your essays for IELTS/TOEFL or any other English text.")

user_text = st.text_area("Enter your text here:", height=200)

if st.button("Analyze Text"):
    if user_text:
        # 1. Определение языка
        try:
            lang = detect(user_text)
        except:
            lang = "unknown"
        
        # 2. Основные метрики
        word_count = len(user_text.split())
        st.subheader("General Metrics")
        col1, col2 = st.columns(2)
        col1.metric("Word Count", word_count)
        col2.metric("Detected Language", lang.upper())

        # 3. Анализ для английского
        if lang == 'en':
            blob = TextBlob(user_text)
            st.subheader("Advanced English Analysis")
            
            # Тональность
            sentiment = blob.sentiment.polarity
            if sentiment > 0.1:
                st.info("Tone: Positive (Good for motivational letters).")
            elif sentiment < -0.1:
                st.warning("Tone: Negative/Critical.")
            else:
                st.write("**Tone:** Neutral/Objective.")

            # Богатство лексики
            # Теперь blob.words заработает благодаря скачанному пункту 'punkt'
            unique_words = len(set(blob.words.lower()))
            lexical_richness = (unique_words / word_count) * 100 if word_count > 0 else 0
            st.write(f"**Lexical Richness:** {lexical_richness:.1f}% unique words.")
            
            if lexical_richness < 40:
                st.error("Tip: Try to use more synonyms to increase your score.")
            else:
                st.success("Tip: Great vocabulary variety!")
        else:
            st.warning("Advanced analysis is only available for English texts.")
    else:
        st.error("Please enter some text first!")
