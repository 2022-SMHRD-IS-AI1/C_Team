from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/join.html')
def join():
    return render_template('join.html')

@app.route('joinservece')
def joinservice():
    


@app.route('/multiFileUploads', methods = ['POST'])
def multi_upload_file():
    if request.method == 'POST':
        upload = request.files.getlist("file[]")
        for f in upload:
            f.save('./uploads/' + secure_filename(f.filename))
            return '파일 저장 완료'
    else:
        return render_template('check.html')

if __name__ == '__main__':
    app.run(port="9999", debug = True)