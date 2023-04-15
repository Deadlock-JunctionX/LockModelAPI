import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer


class IntentionDetector:
    def __init__(self) -> None:
        self.model_uri = "junction-mli"
        self.tokenizer = None
        self.model = None
        self.ready = False

    def load(self) -> bool:
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_uri)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_uri)
        self.ready = True
        return self.ready

    def predict(self, message: str):
        if not self.ready:
            raise Exception("Model is not ready")

        inputs = self.tokenizer(message, return_tensors="pt")

        with torch.no_grad():
            logits = self.model(**inputs).logits

        predicted_class_id = logits.argmax().item()

        return self.model.config.id2label[predicted_class_id]
