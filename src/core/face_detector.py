import cv2
from mtcnn import MTCNN
import os


class FaceDetector:

    def __init__(self):
        self.FACE_HAAR_FEATURE = os.getcwd() + "\src\\features\haarcascade_frontalface_default.xml"
        self.mtcnn = MTCNN()
        self.haar = cv2.CascadeClassifier(self.FACE_HAAR_FEATURE)

    def extract_face(self, detector="mtcnn", image_path=None, image_array=None):
        if image_path is None and image_array is None:
            raise Exception("No image specified")
        if detector == "mtcnn":
            return self._extract_face_mtcnn(image_path, image_array)
        elif detector == "haar":
            return self._extract_face_haar(image_path)

    def _extract_face_mtcnn(self, image_path=None, image_array=None):
        image = None
        if image_path is not None: 
            image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        if image_array is not None:
            image = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)

        faces = self.mtcnn.detect_faces(image)

        if len(faces) != 1:
            raise Exception(
                "Faces is not properly detected, Please try again!")
        
        print(faces)

        (x, y, w, h) = faces[0]['box']
        extracted_face = image[y:(y + h), x:(x + w)]
        return cv2.resize(extracted_face, (160, 160))

    def _extract_face_haar(self, image_path=None, captured=None):
        image = None
        if image_path is not None: 
            image = cv2.cvtColor(cv2.imread(image_path), cv2.COLOR_BGR2RGB)
        if captured is not None:
            image = cv2.cvtColor(captured, cv2.COLOR_BGR2RGB)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.haar.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(200, 200),
                                           flags=cv2.CASCADE_SCALE_IMAGE)

        if len(faces) != 1:
            raise Exception(
                "Faces is not properly detected, Please try again!")

        (x, y, w, h) = faces[0]
        extracted_face = image[y:(y + h), x:(x + w)]
        return cv2.resize(extracted_face, (160, 160))
