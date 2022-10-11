import os
import base64
from PIL import Image
from io import BytesIO
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/compress-image", methods=['POST'])
def compress():
    req = request.get_json()
    imgb64 = req['data']
    imgbyte = base64.b64decode(imgb64)
    img = Image.open(BytesIO(imgbyte))
    x, y = img.size
    base_width = 1366
    if x > base_width or y > base_width:
        percent = base_width / float(x)
        hsize = int((float(y) * float(percent)))
        img = img.resize((base_width, hsize), Image.LANCZOS)

    img.save('compress.jpg')
    file_size = os.stat('compress.jpg').st_size
    with open('compress.jpg', 'rb') as imgr:
        img_base64 = base64.b64encode(imgr.read())
        img_base64 = img_base64.decode('utf-8')

    result = {"data": img_base64, "file_size": file_size}
    os.remove('compress.jpg')
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True, threaded=True)
