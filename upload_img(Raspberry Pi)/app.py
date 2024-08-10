import requests
import subprocess

# Flask 서버의 URL (컴퓨터의 IP 주소와 포트)
url = 'http://아이피 가림:5000/upload'

# 사진을 저장할 경로
image_path = '/home/raspberrypi/Desktop/uploadimg/static/webcam_image.jpg'

# 웹캠으로 사진 찍기
subprocess.run(['fswebcam', '-r', '1280x720', '--jpeg', '85', '-D', '1', image_path])

# 파일을 읽고 POST 요청으로 전송
with open(image_path, 'rb') as image_file:
    files = {'image': image_file}
    response = requests.post(url, files=files)

# 요청 결과 확인
if response.status_code == 200:
    print('이미지 전송 성공:', response.text)
else:
    print('이미지 전송 실패:', response.status_code)
#################################################################
