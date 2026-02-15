import os
import cv2
import numpy as np
from flask import Flask, request
from pyzbar.pyzbar import decode

app = Flask(__name__)

@app.route('/')
def home():
    return "Traffic Verifier Server is Online"

@app.route('/upload', methods=['POST'])
def upload_image():
    # 1. Get image bytes from ESP32
    img_bytes = request.data
    if not img_bytes:
        return "NO_DATA", 400

    # 2. Convert to OpenCV format
    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is not None:
        # 3. Decode QR
        qr_results = decode(img)
        if qr_results:
            qr_data = qr_results[0].data.decode('utf-8')
            print(f"✅ DECODED: {qr_data}")
            return qr_data  # Send text back to ESP32
            
    return "NOT_FOUND"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
