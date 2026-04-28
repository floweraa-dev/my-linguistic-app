import streamlit as st
from textblob import TextBlob
from langdetect import detect
import re

st.set_page_config(page_title="IELTS Writing Assistant", page_icon="🎓", layout="wide")

# Словарь для улучшения лексики (Simple -> Academic)
VOCAB_UPGRADE = {
    "good": ["beneficial", "advantageous", "exemplary"],
    "bad": ["detrimental", "adverse", "substandard"],
    "very": ["extremely", "considerably", "profoundly"],
    "think": ["assert", "believe", "maintain", "opine"],
    "important": ["crucial", "pivotal", "imperative", "paramount"],
    "big": ["substantial", "significant", "vast"],
    "small": ["minuscule", "negligible", "marginal"]
}

def analyze_ielts(text):
    blob = TextBlob(text)
    words = text.lower().split()
    word_count = len(words)
    unique_words = len(set(words))
    
    # 1. Lexical Resource (Словарный запас)
    lex_score = (unique_words / word_count * 10) if word_count > 0 else 0
    
    # 2. Coherence (Длина предложений)
    sentences = text.split('.')
    avg_sent_len = word_count / len(sentences) if len(sentences) > 0 else 0
    coh_score = 9 if 15 < avg_sent_len < 25 else 6
    
    return {
        "word_count": word_count,
        "lex_score": min(9.0, lex_score),
        "coh_score": coh_score,
        "sentiment": blob.sentiment.polarity
    }

st.title("🎓 IELTS Writing Grader & Optimizer")
st.markdown("---")

# Интерфейс с колонками
col_input, col_results = st.columns([2, 1])

with col_input:
    user_text = st.text_area("Paste your IELTS Essay here:", height=350, placeholder="In today's world, it is often argued that...")
    
    if st.button("🚀 Run Deep Analysis"):
        if user_text:
            try:
                if detect(user_text) != 'en':
                    st.warning("Please write in English for accurate IELTS grading.")
                else:
                    results = analyze_ielts(user_text)
                    
                    # Вкладки для результатов
                    tab1, tab2, tab3 = st.tabs(["📊 Score Estimation", "vocabulary_fix" "🔍 Vocabulary Fix", "💡 Tips"])
                    
                    with tab1:
                        st.subheader("Estimated Band Score")
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Lexical Resource", f"{results['lex_score']:.1;}")
                        c2.metric("Coherence", f"{results['coh_score']}.0")
                        c3.metric("Word Count", results['word_count'])
                        
                        if results['word_count'] < 250:
                            st.error("Warning: Task 2 essays must be at least 250 words!")

                    with tab2:
                        st.subheader("Word Upgrades")
                        found_simple = False
                        for simple, better in VOCAB_UPGRADE.items():
                            if re.search(rf"\b{simple}\b", user_text.lower()):
                                st.write(f"❌ Don't use **'{simple}'**. Try: {', '.join([f'*{b}*' for b in better])}")
                                found_simple = True
                        if not found_simple:
                            st.success("No basic words found. Your vocabulary is sophisticated!")

                    with tab3:
                        st.subheader("Personalized Tips")
                        if results['sentiment'] > 0.5:
                            st.info("Your essay is very positive. For IELTS, try to maintain a more academic, neutral tone.")
                        if results['coh_score'] < 7:
                            st.write("- Your sentences might be too short. Try using connectors like *'Furthermore'*, *'However'*, or *'Consequently'*.")

            except Exception as e:
                st.error(f"Error analyzing text: {e}")
        else:
            st.error("Text area is empty!")

with col_results:
    st.sidebar.title("Project Info")
    st.sidebar.info("This tool uses Natural Language Processing (NLP) to help students prepare for TOEFL/IELTS exams.")
    [span_1](start_span)st.sidebar.write(f"Target Score: 1400 (SAT Equiv.)")[span_1](end_span)
