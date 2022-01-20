from flask import Blueprint, render_template
import pickle
from datetime import datetime

from app import camera, face_detector, face_encoder, face_recognizer
from api.controllers.attendance import AttendanceController
from api.controllers.user import UserController

attendance = Blueprint('attendance', __name__, template_folder='templates')

user_controller = UserController()
attendance_controller = AttendanceController()


def recognize_user(face_embedding):
    users = user_controller.fetch_all()
    print(users)

    user_similarities = []

    for user in users:
        anchor_face_embedding = user.encoding.vector
        if anchor_face_embedding is not None:
            user_similarities.append((user, face_recognizer.compare(
                face_embedding, pickle.loads(anchor_face_embedding))))

    print(user_similarities)

    max_similarity_user = max(user_similarities, key=lambda tuple: tuple[1])
    max_similarity_percentage = max_similarity_user[1]

    print("Maximum similarity: {}".format(max_similarity_percentage))

    if max_similarity_percentage > 0.97:
        checked_in_user = max_similarity_user[0]
        print("User: {}".format(checked_in_user))
        return checked_in_user

    return None


@attendance.route('/')
def view():
    attendance_list = attendance_controller.fetch_all()
    return render_template('view-attendance.html', attendance_list=attendance_list)


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
            user_attendance = attendance_controller.fetch_user_today_attendance(
                user_id=recognized_user.id, time=current_time)
            if user_attendance:
                return "Hello, {}! You have already checked in on {}".format(
                    recognized_user.name, user_attendance.check_in_time.strftime("%A, %d %B %Y %I:%M%p"))
            else:
                attendance_controller.check_in(
                    user_id=recognized_user.id, time=current_time)
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
            user_attendance = attendance_controller.fetch_user_today_attendance(
                user_id=recognized_user.id, time=current_time)
            if user_attendance:
                if user_attendance.check_out_time is not None:
                    return "Hello, {}! You have already checked out on {}".format(
                        recognized_user.name, user_attendance.check_in_time.strftime("%A, %d %B %Y %I:%M%p"))

                attendance_controller.check_out(
                    user_id=recognized_user.id, time=current_time)
                return "Hello, {}! You check out on {}".format(
                    recognized_user.name, user_attendance.check_in_time.strftime("%A, %d %B %Y %I:%M%p"))
            else:
                return "Hello, {}! You haven't checked in on {}".format(
                    recognized_user.name, current_time.strftime("%A, %d %B %Y"))

    except:
        return "Face not found. Please try again!"
