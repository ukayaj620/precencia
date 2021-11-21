from flask import Flask, Response, request
from flask.templating import render_template
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

face_detector = FaceDetector()
face_encoder = FaceEncoder()
face_comparator = FaceRecognizer()

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


@app.route('/capture_frame')
def capture_frame():
    _, frame = camera.read()

    try:
        extracted_face = face_detector.extract_face(image_array=frame)
        print(extracted_face)
        cv2.imwrite('captured_capture_frame.jpg', img=extracted_face)
        ret, buffer = cv2.imencode('.jpg', img=extracted_face)
        base64FaceImage = base64.b64encode(buffer)
    except:
        return "Error"

    return base64FaceImage


@app.route('/add-user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        payload = request.form
        image_bytes = base64.b64decode(payload['faceBase64String'])
        image_arr = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_arr, flags=cv2.IMREAD_COLOR)
        cv2.imwrite('captured_add_user.jpg', img=image)
        print(face_encoder.get_embedding(image_array=image))
        byte_array = pickle.dumps(face_encoder.get_embedding(image_array=image))
        print(byte_array)
        print(len(str(byte_array)))
        print(pickle.loads(byte_array))
        print(pickle.loads(byte_array).shape)

    return render_template('add-user.html')



if __name__ == "__main__":
    app.run(debug=True)
