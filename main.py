from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import socket

# 터미널에서 python 파일 실행하기
# 1. cd : 폴더 이동
#         .py 파일있는 곳으로 이동
# 2. python 파일명.py

app = Flask(__name__) # Flask 객체 생성
# __name__ : 현재 파일 이름

# JSP/Servlet 요청 처리 --> URLMapping --> @WebServlet("/login")

# app.route() : Servlet
@app.route('/file_upload', # URLMapping
            methods = ['GET', 'POST']) # request methods : get? post?
def file_upload(): #Service 메서드
    if request.method == 'POST': # POST 방식 요청

        # data라는 이름의 데이터 가져오기
        # {'data': '123'} 
        # print( dict(request.form)['data'] )


        f = request.files['file'] # multipart/form-data 형식의 파일 가져오기
        f.save(secure_filename(f.filename)) # file 저장
      #  return """
      #      {
      #          "data" : "123"
      #      }
      #  """ # return 문자열 == 응답내용, 기본형식은 text/html --> REST API / JSON 형식으로 데이터 제공
     
    else: # GET 방식 요청
        # data라는 이름의 데이터 가져오기
        # {'data': '123'} 
    #    try:
     #       print( dict(request.args)['data'] )
      #  except:
       #     print("error")

        return render_template('file_upload.html') # file_upload.html 을 응답
    

if __name__ == '__main__': # 파일 실행시 __name__ --> __main__
    app.run(host = socket.gethostbyname(socket.gethostname()), # host 컴퓨터의 ip 주소
            port="9999", # port 번호, http://ip주소:port번호/
            debug = True) # 수정가능?
