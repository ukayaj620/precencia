import numpy as np

from src.networks.classifier import ClassifierNetwork


class FaceRecognizer:
    def __init__(self):
        self.network = ClassifierNetwork()
        self.network.load_weights()
    
    def compare(self, input_embedding, anchor_embedding):
        difference = self._get_embedding_difference(input_embedding, anchor_embedding)
        return self.network.model.predict(difference)

    def _get_embedding_difference(self, input_embedding, anchor_embedding):
        return np.array([np.array(anchor_embedding - input_embedding).reshape(-1)])
    