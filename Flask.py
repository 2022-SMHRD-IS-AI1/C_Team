from flask import Flask, render_template, request, redirect, url_for, session, flash
import user
import socket
import os

app = Flask(__name__)
app.secret_key = 'qwer1234'

# 웹에서 requiry.html 호출 시 실행 함수 
@app.route('/requiry.html', methods = ['GET','POST'])
def requiry():
    try:
        return render_template('requiry.html')
    except:
        print('requiry 오류발생!')

# 웹에서 pay 호출 시 실행 함수 
@app.route('/pay', methods = ['GET','POST'])
def pay():
    try:
        return render_template('pay.html')
    except:
        print('pay 오류발생!')

# 웹에서 price 호출 시 실행 함수 
@app.route('/price', methods = ['GET','POST'])
def price():
    try:
        return render_template('Price.html')
    except:
        print('price 오류발생!')





# 기본 시작페이지    
@app.route('/')
def default():
    return redirect(url_for('main'))

# 웹에서 /main이 호출되면 실행되는 함수 
@app.route('/main', methods = ['GET','POST']) # get, post
def main():
    if request.method == 'POST': # post 방식일때
        upload = request.files.getlist("filename[]")
        request.files
        print(upload)
        user_id = session['user_info'][0]
        os.makedirs(f'./uploads/{user_id}', exist_ok=True)

        for f in upload:
            f.save(f'./uploads/{user_id}/' + f.filename)
            
        return render_template('main.html') # 메인 페이지로 이동
    
    else: # get 방식일때 
        return render_template('main.html') # 메인 페이지로 이동

# 웹에서 login 호출 시 실행 함수
@app.route('/login', methods = ['POST', 'GET'])
def login(): # 로그인 함수
    if request.method == 'POST':
        id = request.form['id'] # id값을 저장하는 변수 
        pw = request.form['pw'] # pw값을 저장하는 변수
        result = user.login(id, pw) #user.py의 login 함수불러와 저장 

        if len(result) > 0: # 저장된 값이 존재할때 
            session['user_info'] = result # session 저장
            print(session['user_info'])
            print("로그인에 성공하셨습니다.")
            return redirect(url_for('main')) # main 호출
        
        else: # 값이 존재하지 않음
            print("로그인이 실패했습니다.")
            flash("로그인이 실패했습니다.")
            return render_template('login.html') # 로그인 페이지로 이동
    else:
        return render_template('login.html')

# 웹에서 logout 호출되면 실행되는 함수 
@app.route('/logout', methods = ['GET','POST'])
def logout(): # 로그아웃 함수
    session.pop('user_info', None) # 세션에 저장된값 삭제 
    return render_template('main.html') # 메인 페이지로 이동

# 웹에서 join 호출되면 실행되는 함수
@app.route('/join', methods = ['GET','POST'])
def join(): # 회원가입 함수 
    if request.method == 'POST': # post 방식
        id = request.form['id'] # 입력된 id 값 담아주는 변수
        pw = request.form['pw'] # 입력된 pw 값 담아주는 변수
        result = user.join(id, pw) #user.py의 join 함수 불러와 저장 
        print('result :', result)

        if result: # 가입 성공
            print("회원가입에 성공하셨습니다.")
            return redirect(url_for('login')) # login 호출
        
        else: # 가입 실패 
            print("회원가입이 실패했습니다.")
            return redirect(url_for('join')) # join 호출
        
    else: # get 방식
        return render_template('join.html') # 회원가입으로 페이지 이동
    
# 웹에서 mypage 호출 시 실행 함수
@app.route('/mypage', methods = ['GET','POST'])
def mypage(): # 메인 페이지 
    return render_template('mypage.html', user_id = session['user_info'][0]) # 메인 페이지로 이동, 유저 id는 저장된 세션 0번째 컬럼

# 웹에서 drive 호출 시 실행 함수 
@app.route('/drive')
def drive():
    return render_template('drive.html')

if __name__ == '__main__':
    app.run(host = socket.gethostbyname(socket.gethostname()), port="9999")

