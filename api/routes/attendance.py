from flask import Blueprint
import pickle

from app import camera, face_detector, face_encoder, face_recognizer
from api.models import User

attendance = Blueprint('attendance', __name__, template_folder='templates')


def recognize_user(face_embedding):
    users = User().query.all()

    similarities = [face_recognizer.compare(
        face_embedding, pickle.loads(user.encoding)) for user in users]

    print([(users[idx].name, similarity)
          for idx, similarity in enumerate(similarities)])

    max_similarity = max(similarities)

    print("Maximum similarities: {}".format(max_similarity))

    max_similarity_index = similarities.index(max_similarity)

    print(type(max_similarity > 0.99))

    if max_similarity > 0.97:
        checked_in_user = users[max_similarity_index]
        print("User: {}".format(checked_in_user))
        return checked_in_user

    return None


@attendance.route('/check-in')
def check_in():
    _, frame = camera.read()

    result = None

    try:
        extracted_face = face_detector.extract_face(image_array=frame)
        face_embedding = face_encoder.get_embedding(
            image_array=extracted_face)
        print(face_embedding)
        checked_in_user = recognize_user(face_embedding)
        if checked_in_user is None:
            result = "No user found, please add the user to database"
        else:
            result = "Hello, {}. Welcome back!".format(
                checked_in_user.name)
    except:
        result = "Face not found. Please try again!"

    return result
