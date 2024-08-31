from flask import Flask, send_file, request, jsonify
import requests
import os
import subprocess
import datetime

app = Flask(__name__)

# 사진을 저장할 경로 설정
IMAGE_FOLDER = '/home/raspberrypi/Desktop/uploadimg/static'
last_image_path = None

def capture_image():
    global last_image_path

    # 사진을 저장할 폴더가 없으면 생성
    if not os.path.exists(IMAGE_FOLDER):
        os.makedirs(IMAGE_FOLDER)
    
    # 현재 시간을 이용하여 파일 이름 생성
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(IMAGE_FOLDER, f"image_{timestamp}.jpg")
    
    try:
        # fswebcam 명령어를 사용하여 사진 찍기
        subprocess.run(['fswebcam', '-r', '2592x1944', '--jpeg', '85', '-D', '1', '--no-banner', image_path], check=True) #2592x1944 1280x720
        print(f"이미지 저장 성공: {image_path}")
        last_image_path = image_path
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
        return False

@app.route('/')
def index():
    return '''
        <h1>웹캠 제어</h1>
        <button onclick="captureAndSend()">사진 촬영 및 전송</button>
        <br>
        <a href="/download" id="downloadButton">최근 촬영한 사진 다운로드</a>
        <p id="statusMessage"></p>
        <script>
            function captureAndSend() {
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "/capture", true);
                xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
                xhr.onreadystatechange = function() {
                    if (xhr.readyState === 4) {
                        var response = JSON.parse(xhr.responseText);
                        document.getElementById("statusMessage").textContent = response.message;
                    }
                };
                xhr.send();
            }
        </script>
    '''

@app.route('/capture', methods=['POST'])
def capture_and_send():
    if capture_image():
        url = 'http://203.241.246.172:15000/upload'  # 서버 주소 변경 필요 시 여기를 수정
        #url = 'http://192.168.50.156:5000/upload'  # 서버 주소 변경 필요 시 여기를 수정
        send_image(url, last_image_path)
        return jsonify(message="사진이 성공적으로 촬영 및 전송되었습니다!")
    else:
        return jsonify(message="사진 촬영에 실패했습니다.")

@app.route('/download')
def download_image():
    if last_image_path and os.path.exists(last_image_path):
        return send_file(last_image_path, as_attachment=True)
    else:
        return '''
            <h1>다운로드할 사진이 없습니다.</h1>
            <a href="/">뒤로</a>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
