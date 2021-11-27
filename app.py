from flask import Flask, Response, request, url_for, flash
from flask.templating import render_template
from werkzeug.utils import redirect
import cv2
import numpy as np
from dotenv import load_dotenv
import base64
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import pickle

from config import Config
from src.core.face_recognizer import FaceRecognizer
from src.core.face_encoder import FaceEncoder
from src.core.face_detector import FaceDetector

load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

from api.models import User

face_detector = FaceDetector()
face_encoder = FaceEncoder()
face_recognizer = FaceRecognizer()

camera = cv2.VideoCapture(0)


print("All class sucessfully loaded!")


def get_frame():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', img=frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


def get_check_in_user(face_embedding):
    users = User().query.all()

    similarities = [face_recognizer.compare(
        face_embedding, pickle.loads(user.encoding)) for user in users]

    print([(users[idx].name, similarity) for idx, similarity in enumerate(similarities)])
    
    max_similarity = max(similarities)

    print("Maximum similarities: {}".format(max_similarity))

    max_similarity_index = similarities.index(max_similarity)

    print(type(max_similarity > 0.99))

    if max_similarity > 0.97:
        checked_in_user = users[max_similarity_index]
        print("User: {}".format(checked_in_user))
        return checked_in_user
    
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture-frame')
def capture_frame():
    _, frame = camera.read()

    try:
        extracted_face = face_detector.extract_face(image_array=frame)
        print(extracted_face)
        ret, buffer = cv2.imencode('.jpg', img=extracted_face)
        base64FaceImage = base64.b64encode(buffer)
    except:
        return "Error"

    return base64FaceImage


@app.route('/check-in')
def check_in():
    _, frame = camera.read()

    result = None

    try:
        extracted_face = face_detector.extract_face(image_array=frame)
        face_embedding = face_encoder.get_embedding(image_array=extracted_face)
        print(face_embedding)
        checked_in_user = get_check_in_user(face_embedding)
        if checked_in_user is None:
            result = "No user found, please add the user to database"
        else:
            result = "Hello, {}. Welcome back!".format(checked_in_user.name)
    except:
        result = "Face not found. Please try again!"

    return result


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        payload = request.form

        user = User().query.filter_by(email=payload['email']).first()

        if user:
            flash('Email has already existed', 'warning')
            return redirect(url_for('add_user'))

        face_image_bytes = base64.b64decode(payload['faceBase64String'])

        face_image_array = np.frombuffer(face_image_bytes, dtype=np.uint8)
        face_image = cv2.imdecode(face_image_array, flags=cv2.IMREAD_COLOR)
        face_embedding = face_encoder.get_embedding(image_array=face_image)
        face_byte_array = pickle.dumps(face_embedding)

        print(face_embedding)

        db.session.add(User(
            email=payload['email'],
            name=payload['fullName'],
            encoding=face_byte_array
        ))
        db.session.commit()

        user = User().query.filter_by(email=payload['email']).first()

        flash('User has been created', 'primary')
        print(user.encoding)

        print(pickle.loads(user.encoding))
        print(pickle.loads(user.encoding).shape)

    return render_template('add-user.html')


if __name__ == "__main__":
    app.run(debug=True)
