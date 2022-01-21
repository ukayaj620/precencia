from flask import Flask, Response
from flask.templating import render_template
import click
import cv2
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from config import Config
from src.core.face_verificator import FaceVerificator
from src.core.face_encoder import FaceEncoder
from src.core.face_detector import FaceDetector

load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)


face_detector = FaceDetector()
face_encoder = FaceEncoder()
face_recognizer = FaceVerificator()

camera = cv2.VideoCapture(0)


print("All class sucessfully loaded!")


from api.controllers.role import RoleController
from api.controllers.user import UserController

role_controller = RoleController()
user_controller = UserController()

@app.cli.command('seed')
@click.argument('args')
def seed(args):

    if args == 'role':
        role_controller.create(name='user')
        role_controller.create(name='admin')
        print('Role has been seeded')
        return

    if args == 'admin':
        user_controller.create(
            name=Config.DUMMY_ADMIN_NAME,
            email=Config.DUMMY_ADMIN_EMAIL,
            role_id=role_controller.fetch_by_name('admin').id,
            password=Config.DUMMY_ADMIN_PASSWORD
        )
        print('Dummy admin has been seeded')
        return


def get_frame():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            start_point, end_point = face_detector.get_face_boundary(frame)
            cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)
            ret, buffer = cv2.imencode('.jpg', img=frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


@login_manager.user_loader
def load_user(user_id):
    return user_controller.fetch_by_id(user_id)

from api.routes.service import service
app.register_blueprint(service, url_prefix='/')

from api.routes.user import user
app.register_blueprint(user, url_prefix='/user')

from api.routes.admin import admin
app.register_blueprint(admin, url_prefix='/admin')


if __name__ == "__main__":
    app.run(debug=True)
