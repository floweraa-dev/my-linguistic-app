import streamlit as st

st.title("My Study Assistant 📚")
st.write("Это мое первое приложение для анализа текстов!")

text = st.text_area("Вставьте текст на английском (например, ваше эссе):")

if st.button("Проанализировать"):
    words = text.split()
    word_count = len(words)
    st.info(f"Количество слов в тексте: {word_count}")
    
    if word_count > 0:
        st.success("Приложение работает! Скоро мы добавим сюда проверку сложности слов для экзаменов.")
