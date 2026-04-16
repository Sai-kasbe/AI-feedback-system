import streamlit as st
import pandas as pd
from database import *
from agent import *
from translator import translate
from report import generate_pdf
from alerts import check_alert
from score import event_score
from email_alert import send_email
from form_builder import *
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

create_tables()

if "fields" not in st.session_state:
    st.session_state.fields = []

analyzer = SentimentIntensityAnalyzer()

def analyze(text):
    score = analyzer.polarity_scores(text)['compound']
    if score >= 0.05:
        return "Positive", score
    elif score <= -0.05:
        return "Negative", score
    else:
        return "Neutral", score

st.set_page_config(layout="wide")

menu = st.sidebar.radio("Menu", [
    "Home","Create Event","Build Form","Submit Feedback",
    "Upload CSV","Dashboard","AI Report","Chatbot"
])

# HOME
if menu == "Home":
    st.title("AI Event Feedback System")

# CREATE EVENT
elif menu == "Create Event":
    name = st.text_input("Event Name")
    if st.button("Create"):
        c.execute("INSERT INTO events (name) VALUES (?)",(name,))
        conn.commit()
        st.success("Created")

# BUILD FORM
elif menu == "Build Form":
    build_form()

# SUBMIT
elif menu == "Submit Feedback":
    events = pd.read_sql("SELECT * FROM events", conn)
    event = st.selectbox("Event", events['name'])

    render_form()

    text = st.text_area("Feedback")
    image = st.file_uploader("Upload Image")

    if st.button("Submit"):
        text_en = translate(text)
        sentiment, score = analyze(text_en)

        event_id = events[events['name']==event]['id'].values[0]

        c.execute("INSERT INTO feedback VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                  (event_id, text, sentiment, score))
        conn.commit()

        st.success("Submitted")

# CSV
elif menu == "Upload CSV":
    file = st.file_uploader("Upload")

    if file:
        df = pd.read_csv(file)

        for text in df.iloc[:, -1]:
            sentiment, score = analyze(text)
            c.execute("INSERT INTO feedback VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)",
                      (1, text, sentiment, score))

        conn.commit()
        st.success("Uploaded")

# DASHBOARD
elif menu == "Dashboard":
    df = pd.read_sql("SELECT * FROM feedback", conn)

    if len(df):
        st.bar_chart(df['sentiment'].value_counts())

        df['created_at'] = pd.to_datetime(df['created_at'])
        trend = df.groupby(df['created_at'].dt.date)['score'].mean()
        st.line_chart(trend)

        score_val = event_score(df)
        st.metric("Success Score", f"{score_val}%")

        alert = check_alert(df)
        if alert:
            st.error(alert)
            send_email(alert)

        # Power BI
        st.components.v1.iframe("YOUR_POWER_BI_LINK", height=400)

# AI REPORT
elif menu == "AI Report":
    df = pd.read_sql("SELECT * FROM feedback", conn)

    if st.button("Generate"):
        report = generate_report(df)
        st.write(report)

        pdf = generate_pdf(report)
        with open(pdf,"rb") as f:
            st.download_button("Download PDF", f)

# CHATBOT
elif menu == "Chatbot":
    q = st.text_input("Ask")

    if st.button("Ask"):
        st.write(chatbot(q))

    df = pd.read_sql("SELECT * FROM feedback", conn)
    if len(df)>5:
        st.info(auto_agent(df))
