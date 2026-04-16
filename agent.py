import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_report(df):
    data = "\n".join(df['text'])

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Analyze feedback:\n{data}"}]
    )

    return response['choices'][0]['message']['content']


def chatbot(query):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )

    return response['choices'][0]['message']['content']


def auto_agent(df):
    data = "\n".join(df['text'])

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Analyze:\n{data}"}]
    )

    return response['choices'][0]['message']['content']
