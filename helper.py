from PIL import Image
from transformers import pipeline
import io


def check_profanity(text):
    classifier = pipeline("text-classification", model="eliasalbouzidi/distilbert-nsfw-text-classifier")
    # https://huggingface.co/eliasalbouzidi/distilbert-nsfw-text-classifier?text=Bitch+is+doing+threesome
    if not text:
        return False
    result = classifier(text)
    return result[0]['label'] == 'nsfw' and result[0]['score'] > 0.75


def check_nsfw_image(image_file):
    # Open the image file from memory (for files uploaded via Django forms)
    image = Image.open(image_file)

    # Load the Hugging Face NSFW detection model
    classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")

    # Run the image through the classifier
    result = classifier(image)

    # Check if the label is NSFW with a score greater than a threshold (e.g., 0.75)
    return any(item['label'] == 'nsfw' and item['score'] > 0.75 for item in result)
