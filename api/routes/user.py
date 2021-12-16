from flask import Blueprint, flash, url_for, render_template, request
from werkzeug.utils import redirect
import base64
import numpy as np
import cv2
import pickle

from app import camera, face_detector, face_encoder, db
from api.models import User

user = Blueprint('user', __name__, template_folder='templates')

user_model = User()


@user.route('/capture-face')
def capture_face():
    _, frame = camera.read()

    try:
        extracted_face = face_detector.extract_face(image_array=frame)
        ret, buffer = cv2.imencode('.jpg', img=extracted_face)
        base64FaceImage = base64.b64encode(buffer)
    except:
        return "Error"

    return base64FaceImage


@user.route('/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        payload = request.form

        user = user_model.query.filter_by(email=payload['email']).first()

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

        user = user_model.query.filter_by(email=payload['email']).first()

        flash('User has been created', 'primary')
        print(user.encoding)

        print(pickle.loads(user.encoding))
        print(pickle.loads(user.encoding).shape)

    return render_template('add-user.html')