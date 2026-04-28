import streamlit as st
from textblob import TextBlob
from langdetect import detect

st.set_page_config(page_title="IELTS Writing Checker", page_icon="🎓")

# Боковая панель с критериями
st.sidebar.title("IELTS Criteria")
st.sidebar.info("""
**1. Task Response:** Did you answer the question?
**2. Coherence:** Are your ideas connected?
**3. Lexical Resource:** Is your vocabulary varied?
**4. Grammar Range:** Are your sentences complex?
""")

st.title("IELTS Academic Writing Assistant ✍️")
st.write("Paste your Task 2 essay below to check your Lexical Resource and Sentiment.")

# Поле для ввода
essay = st.text_area("Your Essay:", height=300, placeholder="Write at least 250 words...")

# Списки слов для проверки вокабуляра
academic_words = ['furthermore', 'nevertheless', 'consequently', 'subsequently', 'moreover', 'illustrated', 'significant', 'prevalent']
filler_words = ['very', 'good', 'bad', 'really', 'big', 'small']

if st.button("Check My Essay"):
    if essay:
        try:
            lang = detect(essay)
            if lang != 'en':
                st.error("Please provide text in English for IELTS analysis.")
            else:
                word_count = len(essay.split())
                blob = TextBlob(essay)
                
                # Основные показатели
                col1, col2, col3 = st.columns(3)
                col1.metric("Word Count", word_count)
                
                # Процент уникальных слов (Lexical Resource)
                unique_words = len(set(blob.words.lower()))
                lex_richness = (unique_words / word_count) * 100 if word_count > 0 else 0
                col2.metric("Lexical Variety", f"{lex_richness:.1f}%")
                
                # Тональность (для IELTS обычно должна быть нейтральной)
                sentiment = blob.sentiment.polarity
                col3.metric("Objectivity", "High" if -0.2 < sentiment < 0.2 else "Low")

                st.divider()

                # Анализ вокабуляра
                st.subheader("Vocabulary & Cohesion Analysis")
                
                # Проверка на Academic Linking Words
                found_academic = [w for w in academic_words if w in essay.lower()]
                if found_academic:
                    st.success(f"✅ Good use of linking words: {', '.join(found_academic)}")
                else:
                    st.warning("⚠️ Try using more formal linkers (e.g., 'Furthermore', 'Consequently').")

                # Проверка на "слабые" слова
                found_fillers = [w for w in filler_words if w in essay.lower()]
                if found_fillers:
                    st.error(f"❌ Avoid 'weak' words: {', '.join(set(found_fillers))}. Use more precise synonyms.")

                # Вердикт по объему
                if word_count < 250:
                    st.error(f"Warning: Your essay is only {word_count} words. You need at least 250 words for Task 2.")
                else:
                    st.success("Word count is sufficient for Task 2.")

        except:
            st.error("Could not analyze the text. Please try again.")
    else:
        st.info("Please paste your essay to start the analysis.")
