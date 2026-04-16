def check_alert(df):
    neg = len(df[df['sentiment']=="Negative"])
    total = len(df)

    if total > 0 and neg/total > 0.4:
        return "⚠️ High Negative Feedback!"
    return None
