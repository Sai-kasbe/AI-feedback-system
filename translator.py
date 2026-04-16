from deep_translator import GoogleTranslator

def translate(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text
