import os
import numpy as np
from dotenv import load_dotenv

from src.core.face_recognizer import FaceRecognizer
from src.core.face_encoder import FaceEncoder
from src.core.face_detector import FaceDetector


load_dotenv()

face_detector = FaceDetector()
face_encoder = FaceEncoder()
face_comparator = FaceRecognizer()

ANCHOR_PATH = os.getcwd() + str(os.environ.get("EXAMPLE_ANCHOR_PATH"))
INPUT_PATH = os.getcwd() + str(os.environ.get("EXAMPLE_INPUT_PATH"))
extracted_face = face_detector.extract_face(
    detector="mtcnn", image_path=INPUT_PATH)
input_face_embedding = face_encoder.get_embedding(image_array=extracted_face)
anchor_face_embedding = face_encoder.get_embedding(image_path=ANCHOR_PATH)

print(face_comparator.compare(input_face_embedding, anchor_face_embedding))
