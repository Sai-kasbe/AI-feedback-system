import streamlit as st
import pandas as pd
from database import *
from agent import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

create_tables()

analyzer = SentimentIntensityAnalyzer()

def analyze(text):
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.05:
        return "Positive", score
    elif score <= -0.05:
        return "Negative", score
    else:
        return "Neutral", score

# ---------- UI ----------
st.set_page_config(page_title="AI Feedback System", layout="wide")

st.sidebar.title("Navigation")
menu = ["Home", "Submit", "Dashboard", "AI Insights"]
choice = st.sidebar.radio("Go to", menu)

# ---------- HOME ----------
if choice == "Home":
    st.title("🎯 AI Event Feedback System")
    st.write("Smart analysis using Agentic AI")

# ---------- SUBMIT ----------
elif choice == "Submit":
    st.title("📝 Submit Feedback")

    event = st.text_input("Event Name")
    feedback = st.text_area("Your Feedback")

    if st.button("Submit"):
        sentiment, score = analyze(feedback)

        c.execute("INSERT INTO feedback VALUES (?, ?, ?, ?)",
                  (event, feedback, sentiment, score))
        conn.commit()

        st.success(f"Saved! Sentiment: {sentiment}")

# ---------- DASHBOARD ----------
elif choice == "Dashboard":
    st.title("📊 Dashboard")

    df = pd.read_sql("SELECT * FROM feedback", conn)

    if len(df) > 0:
        st.dataframe(df)
        st.bar_chart(df['sentiment'].value_counts())

# ---------- AI ----------
elif choice == "AI Insights":
    st.title("🤖 AI Analyst")

    df = pd.read_sql("SELECT * FROM feedback", conn)

    if st.button("Generate Report"):
        with st.spinner("Analyzing..."):
            result = gpt_analyze(df)
        st.write(result)
