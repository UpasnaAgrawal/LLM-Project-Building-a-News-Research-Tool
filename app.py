import streamlit as st
from langchain_config import llm_chain, get_summary

# ---- Page Setup ----
st.set_page_config(page_title="Equity News Tool", page_icon="📊", layout="centered")

# ---- Background and Styling ----
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .big-title {
        font-size: 42px;
        color: #0e4b75;
        font-weight: 700;
    }
    .subtext {
        font-size: 18px;
        color: #444;
    }
    .stButton > button {
        background-color: #0e4b75;
        color: white;
        padding: 0.6em 1.5em;
        border-radius: 8px;
        font-weight: bold;
        border: none;
    }
    .stTextInput > div > div > input {
        background-color: white;
        padding: 10px;
        border-radius: 6px;
        border: 1px solid #ccc;
    }
    </style>
""", unsafe_allow_html=True)

# ---- Title ----
st.markdown('<div class="big-title">📈 Equity Research News Tool</div>', unsafe_allow_html=True)
st.markdown('<div class="subtext">Enter your query to get the latest news summarized .</div>', unsafe_allow_html=True)

# ---- Trending Topics ----
st.markdown("#### 🔥 Trending Topics")
trending_topics = ["Tesla", "Bitcoin", "IPO", "Federal Reserve",  "AI Stocks"]

# Initialize session state safely
if "query" not in st.session_state:
    st.session_state.query = ""

# Trending topic buttons
cols = st.columns(len(trending_topics))
for i, topic in enumerate(trending_topics):
    if cols[i].button(topic):
        st.session_state.query = topic  # update query value

# ---- Text Input with session value ----
query = st.text_input("🔍 What are you researching today?", value=st.session_state.query)

# ---- News Fetch Button ----
if st.button("📰 Get News Summary"):
    if query:
        try:
            summaries = get_summary(query)
            response = llm_chain.run({'query': query, 'summaries': summaries})
            st.markdown("### 🧾 Summary:")
            st.success(response)
        except Exception as e:
            st.error(f"❌ An error occurred while summarizing: {e}")
    else:
        st.warning("⚠️ Please enter a query first.")
