from flask import Flask, Response, render_template_string
from threading import Condition
import io
from picamera2 import Picamera2
from picamera2.encoders import JpegEncoder
from picamera2.outputs import FileOutput

# Initialize Flask app
app = Flask('Video:8000')

# HTML page for the MJPEG streaming demo
PAGE = """\
<!doctype html>
<html>
<head>
<title>Raspberry Pi Camera Stream</title>
</head>
<body>
<h1>Raspberry Pi Camera Live Stream</h1>
<img src="/stream.mjpg" width="640" height="480" />
</body>
</html>
"""

# Class to handle streaming output
class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()

# MJPEG streaming route
@app.route('/stream.mjpg')
def stream():
    def generate():
        while True:
            with output.condition:
                output.condition.wait()
                frame = output.frame
            yield (b'--FRAME\r\n'
                   b'Content-Type: image/jpeg\r\n'
                   b'Content-Length: ' + f"{len(frame)}".encode() + b'\r\n\r\n' +
                   frame + b'\r\n')
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=FRAME')

# HTML page route
@app.route('/')
def index():
    return render_template_string(PAGE)

if __name__ == '__main__':
    # Create Picamera2 instance and configure it
    picam2 = Picamera2()
    picam2.configure(picam2.create_video_configuration(main={"size": (1296, 972)}))
    output = StreamingOutput()
    picam2.start_recording(JpegEncoder(), FileOutput(output))

    try:
        # Run the Flask app
        app.run(host='0.0.0.0', port=8000, threaded=True)
    finally:
        # Stop recording when the script is interrupted
        picam2.stop_recording()
