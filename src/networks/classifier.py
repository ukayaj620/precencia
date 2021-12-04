import os
import tensorflow as tf
from tensorflow.keras.callbacks import LearningRateScheduler, EarlyStopping
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.optimizers import Adam


class ClassifierNetwork:

    def __init__(self):
        print("[Classifier Network] start to initialize...")
        self.model = Sequential([
            Input(shape=(128,)),
            Dense(32, activation='relu'),
            Dense(1, activation='sigmoid')
        ])
        self.default_weights_path = os.getcwd() + "\src\weights\classifier_keras_weights.h5"
        print("[Classifier Network] finish initialize...")

    def load_weights(self, path=None):
        print("[Classifier Network] start loading weights...")
        weights_path = self.default_weights_path if path is None else path
        self.model.load_weights(weights_path)
        print("[Classifier Network] finish loading weights...")
