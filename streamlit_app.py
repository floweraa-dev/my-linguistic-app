import streamlit as st
import spacy
from textblob import TextBlob
from langdetect import detect

# Загружаем лингвистическую модель (бесплатно)
@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

nlp = load_nlp()

st.title("Advanced Writing Assistant ✍️")
st.write("Improve your academic English without expensive API keys.")

user_input = st.text_area("Paste your essay here:", height=250)

if st.button("Check Writing"):
    if user_input:
        lang = detect(user_input)
        
        if lang == 'en':
            doc = nlp(user_input)
            blob = TextBlob(user_input)
            
            # 1. Поиск "слабых" слов (Overused Words)
            weak_words = ["very", "good", "bad", "really", "thing", "stuff", "nice"]
            found_weak = [token.text.lower() for token in doc if token.text.lower() in weak_words]
            
            st.subheader("Vocabulary Quality")
            if found_weak:
                st.warning(f"Found {len(found_weak)} overused words. Try to replace them with academic synonyms.")
                st.write(f"Words to replace: {', '.join(set(found_weak))}")
            else:
                st.success("Your vocabulary looks strong and academic!")

            # 2. Анализ сложности предложений
            sentences = list(doc.sents)
            avg_len = len(doc) / len(sentences)
            
            st.subheader("Sentence Structure")
            st.write(f"Average sentence length: {avg_len:.1f} words.")
            if avg_len < 12:
                st.info("Your sentences are quite short. For academic writing, try to use more complex structures.")
            
            # 3. Sentiment (Тональность)
            st.subheader("Tone Analysis")
            st.write(f"Objectivity score: {1 - blob.sentiment.subjectivity:.2f} (1.0 is very objective)")

        else:
            st.error("Please use English for advanced analysis.")
