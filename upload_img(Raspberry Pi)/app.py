from flask import Flask, send_file, request, render_template_string
import requests
import os
import subprocess
import datetime

app = Flask(__name__)

# 사진을 저장할 경로 설정
IMAGE_FOLDER = '/home/raspberrypi/Desktop/uploadimg/static'
UPLOAD_URL = 'http://192.168.153.156:5000/upload'  # 서버 주소

def get_image_path_with_timestamp():
    # 현재 시간을 이용하여 파일 이름 생성
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(IMAGE_FOLDER, f"image_{timestamp}.jpg")

def capture_image(image_path):
    try:
        subprocess.run(['fswebcam', '-r', '2592x1944', '--jpeg', '85', '-D', '1', image_path], check=True)
        print(f"이미지 저장 성공: {image_path}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"웹캠 오류: {e}")
        return False

def send_image(url, image_path):
    try:
        with open(image_path, 'rb') as image_file:
            files = {'image': image_file}
            response = requests.post(url, files=files)

            if response.status_code == 200:
                print('이미지 전송 성공')
            else:
                print(f'이미지 전송 실패: {response.status_code}, {response.text}')
    except requests.exceptions.RequestException as e:
        print(f"요청 오류: {e}")

@app.route('/')
def index():
    # 간단한 HTML 페이지를 렌더링하여 버튼 생성
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>사진 촬영 및 전송</title>
        </head>
        <body>
            <h1>사진 촬영 및 전송</h1>
            <button onclick="location.href='/capture_and_send'">사진 촬영 및 전송</button>
            {% if status_message %}
                <p>{{ status_message }}</p>
            {% endif %}
        </body>
        </html>
    ''')

@app.route('/capture_and_send')
def capture_and_send():
    # 현재 시간을 기반으로 이미지 파일 경로 생성
    image_path = get_image_path_with_timestamp()

    # 웹캠으로 사진 찍기
    if capture_image(image_path):
        # 사진 전송
        send_image(UPLOAD_URL, image_path)
        status_message = f"사진 촬영 및 전송 완료: {os.path.basename(image_path)}"
    else:
        status_message = "사진 촬영 실패"

    # 상태 메시지를 index 페이지에 전달
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="ko">
        <head>
            <meta charset="UTF-8">
            <title>사진 촬영 및 전송</title>
        </head>
        <body>
            <h1>사진 촬영 및 전송</h1>
            <button onclick="location.href='/capture_and_send'">사진 촬영 및 전송</button>
            <p>{{ status_message }}</p>
        </body>
        </html>
    ''', status_message=status_message)

if __name__ == '__main__':
    # 사진을 저장할 폴더가 없으면 생성
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)

    app.run(host='0.0.0.0', port=5000)
