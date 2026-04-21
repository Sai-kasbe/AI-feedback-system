import streamlit as st
import pandas as pd
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# ---------- HEADER ----------
st.markdown("""
<div style='background:linear-gradient(90deg,#4f46e5,#9333ea);
padding:20px;border-radius:10px'>
<h1 style='color:white;'>🎯 AI Event Intelligence Dashboard</h1>
<p style='color:white;'>Real insights. Not just charts.</p>
</div>
""", unsafe_allow_html=True)

# ---------- FILE ----------
file = st.file_uploader("Upload Feedback CSV", type=["csv"])

if file:
    df = pd.read_csv(file)

    st.subheader("📄 Preview")
    st.dataframe(df.head())

    col = st.selectbox("Select Feedback Column", df.columns)

    # ---------- CLEAN ----------
    df[col] = df[col].astype(str).str.strip()
    df = df[df[col] != ""]

    # ---------- SAMPLE ----------
    if len(df) > 100000:
        df = df.sample(40000)

    analyzer = SentimentIntensityAnalyzer()

    # ---------- SENTIMENT ----------
    df["score"] = df[col].apply(lambda x: analyzer.polarity_scores(x)["compound"])

    df["Sentiment"] = pd.cut(
        df["score"],
        bins=[-1, -0.05, 0.05, 1],
        labels=["Negative", "Neutral", "Positive"]
    )

    # ---------- KPI ----------
    pos = (df["Sentiment"] == "Positive").sum()
    neg = (df["Sentiment"] == "Negative").sum()
    neu = (df["Sentiment"] == "Neutral").sum()
    total = len(df)

    success = (pos / total) * 100

    st.markdown("## 📊 Event Health")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("😊 Positive", pos)
    c2.metric("😐 Neutral", neu)
    c3.metric("😡 Negative", neg)
    c4.metric("🏆 Success Score", f"{success:.1f}%")

    # ---------- INTERPRETATION ----------
    if success > 75:
        st.success("🔥 Strong Event Performance")
    elif success > 50:
        st.warning("⚠ Moderate Performance – Improvement Needed")
    else:
        st.error("❌ Poor Event Performance")

    # ---------- TREND ----------
    st.markdown("## 📈 Event Trend")

    df["group"] = pd.cut(df.index, bins=25)
    trend = df.groupby("group")["score"].mean()

    fig, ax = plt.subplots()
    ax.plot(trend.values, marker='o')
    ax.set_title("Sentiment Trend")

    st.pyplot(fig)

    if trend.iloc[-1] > trend.iloc[0]:
        st.success("📈 Experience improved over time")
    else:
        st.error("📉 Experience declined over time")

    # ---------- DISTRIBUTION ----------
    st.markdown("## 📊 Sentiment Distribution")
    st.bar_chart(df["Sentiment"].value_counts())

    # ---------- REAL ISSUE EXTRACTION ----------
    st.markdown("## 🔍 Top Issues (From Negative Feedback)")

    neg_df = df[df["Sentiment"] == "Negative"]

    if len(neg_df) > 5:
        tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=20)
        X = tfidf.fit_transform(neg_df[col])

        terms = tfidf.get_feature_names_out()
        scores = X.sum(axis=0).A1

        issues = sorted(zip(terms, scores), key=lambda x: x[1], reverse=True)

        for issue, score in issues[:8]:
            st.write(f"- {issue}")

    else:
        st.write("Not enough negative feedback")

    # ---------- STRENGTHS ----------
    st.markdown("## 💚 What Users Liked")

    pos_df = df[df["Sentiment"] == "Positive"]

    if len(pos_df) > 5:
        tfidf2 = TfidfVectorizer(stop_words="english", ngram_range=(1,2), max_features=15)
        X2 = tfidf2.fit_transform(pos_df[col])

        terms2 = tfidf2.get_feature_names_out()
        scores2 = X2.sum(axis=0).A1

        strengths = sorted(zip(terms2, scores2), key=lambda x: x[1], reverse=True)

        for s, _ in strengths[:6]:
            st.write(f"- {s}")

    # ---------- REAL RECOMMENDATIONS ----------
    st.markdown("## 🤖 Actionable Recommendations")

    recommendations = []

    for issue, _ in issues[:5]:
        if "delay" in issue or "time" in issue:
            recommendations.append("Improve scheduling and reduce delays")

        elif "food" in issue:
            recommendations.append("Enhance food quality and service")

        elif "management" in issue or "organize" in issue:
            recommendations.append("Improve event coordination")

        elif "speaker" in issue:
            recommendations.append("Improve speaker engagement quality")

    if success > 75:
        recommendations.append("Maintain current strengths and scale the event")

    for r in list(set(recommendations)):
        st.write(f"- {r}")

    st.success("✔ Insight generation complete")
