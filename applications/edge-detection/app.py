from flask import Flask, render_template, Response 
import cv2
import torch
import os
from remote_infer_grpc import ort_v5
import time



GRPC_HOST = os.getenv('GRPC_HOST', 'modelmesh-serving.object-detection')
GRPC_PORT = os.getenv('GRPC_PORT', '8033')
MODEL_NAME = os.getenv('MODEL_NAME', 'object-detection')
CONF_THRESHOLD = float(os.getenv('CONF_THRESHOLD', 0.2))
IOU_THRESHOLD = float(os.getenv('IOU_THRESHOLD', 0.5))
CLASSES_FILE = 'classes.yaml'


app = Flask(__name__)
source = 0
camera = cv2.VideoCapture(source)
infer=ort_v5(GRPC_HOST, GRPC_PORT, MODEL_NAME, 640, CLASSES_FILE)

def predict(im):
    result = infer(im, CONF_THRESHOLD, IOU_THRESHOLD)
    return result

def gen_frame():
    while True:
        success, frame = camera.read()
        if not success:
            break 
        else:
            frame = predict(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            #print(frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', threaded=True)
