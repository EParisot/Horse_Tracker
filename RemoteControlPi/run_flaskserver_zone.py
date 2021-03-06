# You MUST run this with python3
# To Run:  python3 run_flaskserver_zone.py

import signal
import sys
import logging
import time
import os
from PIL import Image
import numpy as np
from keras.models import load_model
import tensorflow as tf
import cv2
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import const


# check if it's ran with Python3
assert sys.version_info[0:1] == (3,)

# imports needed for web server
from flask import Flask, jsonify, render_template, request, Response, send_from_directory, url_for
from werkzeug.serving import make_server

# imports needed for stream server
import io
import picamera
import socketserver
from threading import Condition, Thread, Event
from http import server

# imports needed to move
from Step_Motor import Step_Motor

# init motor
zero = const.ZERO
motor = Step_Motor(zero=zero, delay=0.002).start() # def: pins=[4,17,27,22], delay=0.001, zero=3
command = zero

logging.basicConfig(level = logging.DEBUG)

# for triggering the shutdown procedure when a signal is detected
keyboard_trigger = Event()
def signal_handler(signal, frame):
    logging.info('Signal detected. Stopping threads.')
    keyboard_trigger.set()

#######################
### Web Server Stuff ##
#######################

# Directory Path can change depending on where you install this file.  Non-standard installations
# may require you to change this directory.
directory_path = 'static'

HOST = "0.0.0.0"
WEB_PORT = 5000
app = Flask(__name__, static_url_path='')

class WebServerThread(Thread):
    '''
    Class to make the launch of the flask server non-blocking.
    Also adds shutdown functionality to it.
    '''
    def __init__(self, app, host, port):
        Thread.__init__(self)
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        logging.info('Starting Flask server')
        self.srv.serve_forever()

    def shutdown(self):
        logging.info('Stopping Flask server')
        self.srv.shutdown()

class Position(object):
    def __init__(self):
        self.x = 0
        self.y = 0
        self.rec = 0
        self.mode = 0

pos = Position()

@app.route("/tracker", methods = ["POST"])
def commands():
    # get the query
    args = request.args
    
    pos.x = float(args['x'])
    pos.y = float(args['y'])
    pos.rec = args['rec']
    pos.mode = args['mode']
    
    ###############################################
    #controls
    if pos.mode == '0':
        command = int(round(pos.x * 2 * zero, 0))
        motor.update(command)

    ###############################################

    resp = Response()
    resp.mimetype = "application/json"
    resp.status = "OK"
    resp.status_code = 200
    return resp

@app.route("/")
def index():
    return page("index_zone.html")

@app.route("/<string:page_name>")
def page(page_name):
    return render_template("{}".format(page_name))

@app.route("/static/<path:path>")
def send_static(path):
    return send_from_directory(directory_path, path)

#############################
### Video Streaming Stuff ###
#############################

class StreamingOutput(object):
    '''
    Class to which the video output is written to.
    The buffer of this class is then read by StreamingHandler continuously.
    '''
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

class StreamingHandler(server.BaseHTTPRequestHandler):
    '''
    Implementing GET request for the video stream.
    '''
    def __init__(self, *args, **kwargs):
        self.model = None
        self.graph = None
        super().__init__(*args, **kwargs)
        
    def draw_circle(self, np_img, x_pred, y_pred):
        w = int(self.model.layers[-2].output_shape[-1])
        h = int(self.model.layers[-1].output_shape[-1])
        x = int(np_img.shape[1] / w) * x_pred + int((np_img.shape[1] / w) / 2)
        y = int(np_img.shape[0] / h) * y_pred + int((np_img.shape[0] / h) / 2)
        cv2.circle(np_img,(x, y), 50, (0, 255, 0), 2)
        img = Image.fromarray(np_img)
        with io.BytesIO() as output:
            img.save(output, format="JPEG")
            img = output.getvalue()
        return img
    
    def make_prediction(self, np_img):
        global motor
        if self.model == None:
            logging.info("Auto mode : Loading Model ...")
            self.model = load_model(os.path.join("../", const.MODEL))
            self.graph = tf.get_default_graph()
            logging.info("Model Loaded")
        image = np.array([np_img / 255.0])
        with self.graph.as_default():
            pred = self.model.predict(image)
        pres = np.argmax(pred[0])
        x_pred = np.argmax(pred[1])
        y_pred = np.argmax(pred[2])
        if pres == 1:
            motor.update(x_pred)
        else:
            motor.update(const.ZERO)
        logging.info("Prediction : %d ; %d" % (int(x_pred), int(y_pred)))
        return self.draw_circle(np_img, x_pred, y_pred)
    
    def do_GET(self):
        if self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                stamp = time.time()
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    # Save video images with labels
                    if pos.rec == '1' and time.time() - stamp >= 0.1:
                        # Record images at 10 fps
                        stamp = time.time()
                        dataBytesIO = io.BytesIO(frame)
                        img = Image.open(dataBytesIO)
                        img.save(os.path.join("output", str(time.time()) + '_1_' + str(round(pos.x, 2)) + '_' + str(round(pos.y, 2)) + ".png"))
                    # Make prediction
                    if pos.mode == '1':
                        dataBytesIO = io.BytesIO(frame)
                        img = Image.open(dataBytesIO)
                        np_img = np.asarray(img)
                        frame = self.make_prediction(np_img)
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

#############################
### Aggregating all calls ###
#############################

if __name__ == "__main__":
    # registering both types of signals
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # firing up the video camera (pi camera)
    camera = picamera.PiCamera(resolution=str(const.RESOLUTION[0]) + "x" + str(const.RESOLUTION[1]),
                               framerate=const.FPS)
    output = StreamingOutput()
    camera.start_recording(output, format='mjpeg')
    logging.info("Started recording with picamera")
    STREAM_PORT = 5001
    stream = StreamingServer((HOST, STREAM_PORT), StreamingHandler)

    # starting the video streaming server
    streamserver = Thread(target = stream.serve_forever)
    streamserver.start()
    logging.info("Started stream server for picamera")

    # starting the web server
    webserver = WebServerThread(app, HOST, WEB_PORT)
    webserver.start()
    logging.info("Started Flask web server")

    # and run it indefinitely
    while not keyboard_trigger.is_set():
        time.sleep(0.1)

    # until some keyboard event is detected
    logging.info("Keyboard event detected")

    # trigger shutdown procedure
    motor.stop()
    webserver.shutdown()
    camera.stop_recording()
    stream.shutdown()

    # and finalize shutting them down
    webserver.join()
    streamserver.join()
    logging.info("Stopped all threads")

    sys.exit(0)
