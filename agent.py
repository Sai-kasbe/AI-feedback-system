import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def gpt_analyze(df):
    feedback_text = "\n".join(df['text'].tolist())

    prompt = f"""
    You are an expert event analyst AI.

    Analyze this feedback:
    {feedback_text}

    Give:
    - Summary
    - Problems
    - Positive points
    - Improvements
    - Future ideas
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content
