import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_report(df):
    data = "\n".join(df['text'])

    prompt = f"""
    Analyze event feedback:
    {data}

    Give:
    - Overall performance
    - Problems
    - Strengths
    - Suggestions
    - Future ideas
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content


def chatbot(query):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )
    return res.choices[0].message.content


def auto_agent(df):
    data = "\n".join(df['text'])

    prompt = f"""
    Analyze feedback:
    {data}

    Detect:
    - Issues
    - Suggestions
    - Event success prediction
    """

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return res.choices[0].message.content
