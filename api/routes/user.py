from flask import Blueprint, flash, url_for, render_template, request
from flask_login import login_required
from werkzeug.utils import redirect
import base64
import numpy as np
import cv2
import pickle

from app import camera, face_detector, face_encoder
from api.controllers.user import UserController
from api.controllers.role import RoleController

user = Blueprint('user', __name__, template_folder='templates')

user_controller = UserController()
role_controller = RoleController()


@user.route('/detect-face')
@login_required
def detect_face():
    _, frame = camera.read()

    try:
        extracted_face = face_detector.extract_face(image_array=frame)
        ret, buffer = cv2.imencode('.jpg', img=extracted_face)
        base64FaceImage = base64.b64encode(buffer)
    except:
        return "Error"

    return base64FaceImage


@user.route('/', methods=['GET', 'POST'])
@login_required
def index():
    users = user_controller.fetch_all()
    return render_template('admin/user/index.html', users=users)


@user.route('/create', methods=['POST'])
def create():
    payload = request.form
    user = user_controller.fetch_by_email(email=payload['email'])
    if user:
        flash('Email has already existed', 'warning')
    else:
        user_controller.create(
            name=payload['fullName'],
            email=payload['email'],
            role_id=role_controller.fetch_by_name('user').id,
        )
        flash('User has been created', 'primary')

    return redirect(url_for('admin.user.index'))


@user.route('/capture-face', methods=['POST'])
@login_required
def capture_face():
    payload = request.form
    user = user_controller.fetch_by_id(id=payload['userId'])
    print(user)
    return render_template('admin/user/face.html', user=user)


@user.route('/store-face', methods=['POST'])
@login_required
def store_face():
    payload = request.form

    user = user_controller.fetch_by_id(id=payload['userId'])
    face_image_bytes = base64.b64decode(payload['faceBase64String'])

    face_image_array = np.frombuffer(face_image_bytes, dtype=np.uint8)
    face_image = cv2.imdecode(face_image_array, flags=cv2.IMREAD_COLOR)
    face_embedding = face_encoder.get_embedding(image_array=face_image)
    face_byte_array = pickle.dumps(face_embedding)

    user_controller.update_face_embedding(
        user_id=user.id,
        embedding=face_byte_array
    )

    flash("User {}'s face has been stored".format(user.name), 'primary')

    return redirect(url_for('admin.user.index'))
