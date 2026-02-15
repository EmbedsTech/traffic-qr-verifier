from flask import Flask, request, Response
import cv2
import numpy as np
from pyzbar.pyzbar import decode

app = Flask(__name__)

# Global variable to store the latest frame
latest_frame = None

def generate_frames():
    global latest_frame
    while True:
        if latest_frame is not None:
            # Encode the frame back to JPEG for the browser
            ret, buffer = cv2.imencode('.jpg', latest_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    # Simple HTML to show the stream
    return "<html><body><h1>ESP32-CAM Live Stream</h1><img src='/video_feed' width='640'></body></html>"

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/upload', methods=['POST'])
def upload_image():
    global latest_frame
    img_bytes = request.data
    if not img_bytes:
        return "NO_DATA", 400

    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is not None:
        latest_frame = img.copy() # Update the frame for the web stream
        
        # Optional: Draw a box around the QR code in the Python window
        qr_results = decode(img)
        if qr_results:
            qr_data = qr_results[0].data.decode('utf-8')
            print(f"✅ Decoded: {qr_data}")
            return qr_data
    
    return "NOT_FOUND"

if __name__ == '__main__':
    app.run(host='10.23.101.67', port=5000, debug=False, threaded=True)
