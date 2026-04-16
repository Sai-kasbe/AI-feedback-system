def event_score(df):
    pos = len(df[df['sentiment']=="Positive"])
    total = len(df)

    if total == 0:
        return 0

    return round((pos/total)*100, 2)
