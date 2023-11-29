from flask import Flask, render_template, Response 
import cv2
import torch
import os
import time


app = Flask(__name__)
source = 0
camera = cv2.VideoCapture(source)
model = torch.hub.load('yolov5', 'custom', path='model/model.pt', source='local') 
model.conf = float(os.getenv('CONF_THRESHOLD', 0.65))
FRAME_INTERVAL = float(os.getenv('FRAME_INTERVAL', 1))

def predict(im):
    result = model(im, size=640)
    result.render()
    return result.ims[0]

def gen_frame():
    while True:
        time.sleep(FRAME_INTERVAL)
        success, frame = camera.read()
        if not success:
            break 
        else:
            start = time.time()
            frame = predict(frame)
            inf_time = time.time() - start
            print(f"Inference took: {inf_time}ms")
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
