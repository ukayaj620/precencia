from operator import and_
from flask import Blueprint
import pickle
from datetime import datetime

from app import camera, face_detector, face_encoder, face_recognizer, db
from api.models import User, Attendance

attendance = Blueprint('attendance', __name__, template_folder='templates')

user_model = User()
attendance_model = Attendance()


def recognize_user(face_embedding):
    users = user_model.query.all()

    similarities = [face_recognizer.compare(
        face_embedding, pickle.loads(user.encoding)) for user in users]

    print([(users[idx].name, similarity)
          for idx, similarity in enumerate(similarities)])

    max_similarity = max(similarities)

    print("Maximum similarities: {}".format(max_similarity))

    max_similarity_index = similarities.index(max_similarity)

    if max_similarity > 0.97:
        checked_in_user = users[max_similarity_index]
        print("User: {}".format(checked_in_user))
        return checked_in_user

    return None


@attendance.route('/check-in')
def check_in():
    _, frame = camera.read()

    try:
        extracted_face = face_detector.extract_face(image_array=frame)
        face_embedding = face_encoder.get_embedding(
            image_array=extracted_face)
        print(face_embedding)
        recognized_user = recognize_user(face_embedding)
        if recognized_user is None:
            return "No user found, please add the user to database"
        else:
            current_time = datetime.now()
            user_attendance = attendance_model.query.filter_by(
                user_id=recognized_user.id, attendance_date=current_time.date()).first()
            if user_attendance:
                return "Hello, {}! You have already checked in on {}".format(
                    recognized_user.name, user_attendance.check_in_time.strftime("%A, %d %B %Y %I:%M%p"))
            else:
                db.session.add(Attendance(
                    user_id=recognized_user.id,
                    attendance_date=current_time.date(),
                    check_in_time=current_time
                ))
                db.session.commit()
                return "Hello, {}! You check in on {}".format(
                    recognized_user.name, current_time.strftime("%A, %d %B %Y %I:%M%p"))
    
    except:
        return "Face not found. Please try again!"



@attendance.route('/check-out')
def check_out():
    _, frame = camera.read()

    try:
        extracted_face = face_detector.extract_face(image_array=frame)
        face_embedding = face_encoder.get_embedding(
            image_array=extracted_face)
        print(face_embedding)
        recognized_user = recognize_user(face_embedding)
        if recognized_user is None:
            return "No user found, please add the user to database"
        else:
            current_time = datetime.now()
            user_attendance = attendance_model.query.filter_by(
                user_id=recognized_user.id, attendance_date=current_time.date()).first()
            if user_attendance:
                if user_attendance.check_out_time is not None:
                    return "Hello, {}! You have already checked out on {}".format(
                    recognized_user.name, user_attendance.check_in_time.strftime("%A, %d %B %Y %I:%M%p"))

                user_attendance.check_out_time = current_time
                db.session.commit()
                return "Hello, {}! You check out on {}".format(
                    recognized_user.name, user_attendance.check_in_time.strftime("%A, %d %B %Y %I:%M%p"))
            else:
                return "Hello, {}! You haven't checked in on {}".format(
                    recognized_user.name, current_time.strftime("%A, %d %B %Y"))

    except:
        return "Face not found. Please try again!"
