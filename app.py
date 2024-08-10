from flask import Flask, request
import os

app = Flask(__name__)

# 이미지 저장 경로 (Windows 바탕화면)
UPLOAD_FOLDER = r'C:\Users\사용자이름\Desktop'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return 'No image part in the request', 400

    file = request.files['image']

    if file.filename == '':
        return 'No selected file', 400

    # 파일 저장
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    return f'Image saved as {file.filename}', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
