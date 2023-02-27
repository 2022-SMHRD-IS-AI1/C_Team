from flask import Flask, request, send_file
from ftplib import FTP

app = Flask(__name__)
ftp = FTP('ftp.example.com')  # FTP 서버 정보 입력
ftp.login(user='username', passwd='password')  # FTP 로그인 정보 입력

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']  # 업로드한 파일 가져오기
    ftp.storbinary('STOR ' + file.filename, file)  # FTP 서버에 파일 업로드
    return 'File uploaded successfully!'

@app.route('/download/<filename>')
def download(filename):
    local_filename = 'downloads/' + filename  # 다운로드할 파일 경로 설정
    with open(local_filename, 'wb') as f:
        ftp.retrbinary('RETR ' + filename, f.write)  # FTP 서버에서 파일 다운로드
    return send_file(local_filename, as_attachment=True)  # 다운로드할 파일 전송

if __name__ == '__main__':
    app.run()