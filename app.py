from flask import Flask, render_template, request, redirect, url_for
#import os
#from werkzeug.utils import secure_filename


app = Flask(__name__)


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

@app.route('/mypage.html', methods = ['GET','POST'])
def mypage():
    try:
        return render_template('Mypage.html')
    except:
        print('mypage 오류발생!')

@app.route('/login.html', methods = ['GET','POST'])
def login():
    try:
        return render_template('login.html')
    except:
        print('login 오류발생!')

@app.route('/join.html', methods = ['GET','POST'])
def join():
    try:
        return render_template('Join.html')
    except:
        print('join 오류발생!')

@app.route('/main.html', methods = ['GET','POST'])
def main():
    try:
        return render_template('Main.html')
    except:
        print("main 오류발생!")
    

if __name__ == '__main__':
    app.run(port="9999", debug = True)