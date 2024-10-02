from transformers import pipeline


class CachedNSFWModel:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self.classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")

    def classify(self, image):
        return self.classifier(image)[0]
