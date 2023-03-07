from flask import Flask, render_template, request, redirect, url_for, session
import user
import socket
#import os
#from werkzeug.utils import secure_filename


app = Flask(__name__)
app.secret_key = 'qwer1234'

# @app.route('/multiFileUploads', methods = ['POST'])
# def multi_upload_file():
#     if request.method == 'POST':
#         upload = request.files.getlist("file[]")
#         for f in upload:
#             f.save('./uploads/' + secure_filename(f.filename))
#             return '파일 저장 완료'
#     else:
#         return render_template('check.html')


@app.route('/requiry.html', methods = ['GET','POST'])
def requiry():
    try:
        return render_template('requiry.html')
    except:
        print('requiry 오류발생!')

@app.route('/pay.html', methods = ['GET','POST'])
def pay():
    try:
        return render_template('pay.html')
    except:
        print('pay 오류발생!')

@app.route('/price.html', methods = ['GET','POST'])
def price():
    try:
        return render_template('Price.html')
    except:
        print('price 오류발생!')





    
@app.route('/')
def default():
    return redirect(url_for('main'))

@app.route('/main', methods = ['GET','POST'])
def main():
    if request.method == 'POST':
        return render_template(('main.html'))
        
    else:
        return render_template('main.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
    
        id = request.form['id'] 
        pw = request.form['pw']

        result = user.login(id, pw)

        if len(result) > 0:
            print("로그인에 성공하셨습니다.")
            session['user_info'] = result
            print(session['user_info'])
            return redirect(url_for('main'))
        else:
            print("로그인이 실패했습니다.")
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/logout', methods = ['GET','POST'])
def logout():
    session.pop('user_info', None)
    return render_template('main.html')

@app.route('/join', methods = ['GET','POST'])
def join():
    if request.method == 'POST':
        id = request.form['id'] 
        pw = request.form['pw']
    
        result = user.join(id, pw)

        if result:
            print("회원가입에 성공하셨습니다.")
            return redirect(url_for('login'))
        else:
            print("회원가입이 실패했습니다.")
            return redirect(url_for('join'))
    else:
        return render_template('join.html')

@app.route('/mypage.html', methods = ['GET','POST'])
def mypage():
    return render_template('mypage.html', user_id = session['user_info'][0])

if __name__ == '__main__':
    app.run(host = socket.gethostbyname(socket.gethostname()), port="9999")

