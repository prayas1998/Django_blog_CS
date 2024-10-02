from PIL import Image
from transformers import pipeline
import io

from ml_models import CachedNSFWModel


def check_profanity(text):
    classifier = pipeline("text-classification", model="eliasalbouzidi/distilbert-nsfw-text-classifier")
    # https://huggingface.co/eliasalbouzidi/distilbert-nsfw-text-classifier?text=Bitch+is+doing+threesome
    if not text:
        return False
    result = classifier(text)
    return result[0]['label'] == 'nsfw' and result[0]['score'] > 0.75


def check_image_nsfw(uploaded_file):
    if not uploaded_file:
        return False

    try:
        image_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(image_bytes))

        classifier = CachedNSFWModel.get_instance()
        result = classifier.classify(image)

        return result['label'] == 'nsfw' and result['score'] > 0.75
    except Exception as e:
        print(f"Error classifying the image: {e}")
        return None
    finally:
        uploaded_file.seek(0)
