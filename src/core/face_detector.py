import cv2
from mtcnn import MTCNN
import os


class FaceDetector:

    def __init__(self):
        print("[MTC Network] starting....")
        self.mtcnn = MTCNN()
        print("[MTC Network] finish initialization....")

    def get_face_boundary(self, frame):
        try:
            faces = self.mtcnn.detect_faces(frame)
        except:
            print("There is a problem when detecting face. Please try again!")
        
        if len(faces) != 1:
            return (0, 0), (0, 0)
        
        (x, y, w, h) = faces[0]['box']
        return (x, y), (x + w, y + h)
        
    def extract_face(self, image_path=None, image_array=None):
        if image_path is None and image_array is None:
            raise Exception("No image specified")
        
        print("Extraction in progress")

        return self._extract_face_mtcnn(image_path, image_array)

    def _extract_face_mtcnn(self, image_path=None, image_array=None):
        image = None
        if image_path is not None: 
            image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        if image_array is not None:
            image = image_array
        
        print("[MTCNN] Image loading done")

        try:
            faces = self.mtcnn.detect_faces(image)
        except:
            print("There is a problem when detecting face. Please try again!")

        if len(faces) != 1:
            raise Exception(
                "Either zero face or more than one faces are detected. Please try again!")
        
        print("[MTCNN] Face is detected")

        (x, y, w, h) = faces[0]['box']
        extracted_face = image[y:(y + h), x:(x + w)]
        return cv2.resize(extracted_face, (160, 160))
