import streamlit as st
from textblob import TextBlob

st.set_page_config(page_title="Study Assistant", page_icon="📚")

st.title("My Study Assistant 📚")
st.write("Это твой личный инструмент для анализа академических текстов.")

text = st.text_area("Вставьте текст на английском (например, ваше эссе):", height=200)

if st.button("Проанализировать"):
    if text:
        # 1. Считаем базовые показатели
        words = text.split()
        word_count = len(words)
        avg_word_len = sum(len(word) for word in words) / word_count if word_count > 0 else 0
        
        # 2. Анализируем тональность через TextBlob
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        
        # Выводим результат
        st.subheader("Результаты анализа:")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Слов", word_count)
        col2.metric("Ср. длина слова", round(avg_word_len, 1))
        
        if sentiment > 0.1:
            col3.write("Тон: Позитивный 😊")
        elif sentiment < -0.1:
            col3.write("Тон: Критический 🧐")
        else:
            col3.write("Тон: Нейтральный 😐")

        # Совет для IELTS/TOEFL
        st.info("💡 **Совет:** Если средняя длина слова меньше 5.0, попробуйте использовать более сложную академическую лексику.")
    else:
        st.warning("Пожалуйста, введите текст!")
