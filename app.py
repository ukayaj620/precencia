from flask import Flask, Response
from flask.templating import render_template
import cv2
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from config import Config
from core.face_verificator import FaceVerificator
from src.core.face_encoder import FaceEncoder
from src.core.face_detector import FaceDetector

load_dotenv()

db = SQLAlchemy()

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
migrate = Migrate(app, db)


face_detector = FaceDetector()
face_encoder = FaceEncoder()
face_recognizer = FaceVerificator()

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


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video')
def video():
    return Response(get_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


from api.models import User, Attendance

from api.routes.attendance import attendance
app.register_blueprint(attendance, url_prefix='/attendance')

from api.routes.user import user
app.register_blueprint(user, url_prefix='/user')


if __name__ == "__main__":
    app.run(debug=True)
