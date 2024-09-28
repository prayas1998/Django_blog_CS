from transformers import pipeline

def check_profanity(text):
    classifier = pipeline("text-classification", model="eliasalbouzidi/distilbert-nsfw-text-classifier")
    # https://huggingface.co/eliasalbouzidi/distilbert-nsfw-text-classifier?text=Bitch+is+doing+threesome
    if not text:
        return False
    result = classifier(text)
    return result[0]['label'] == 'nsfw' and result[0]['score'] > 0.75