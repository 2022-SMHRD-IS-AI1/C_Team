from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

import cx_Oracle
import os #디렉토리 절대 경로
from flask import Flask, render_template, request, redirect

# 라이브러리 위치 정보
cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\smhrd\Oracle\instantclient_21_9")
# Flask 객체생성
app = Flask(__name__)

# 한글 가능하게
os.putenv('NLS_LANG', '.UTF8')
# 데이터 베이스 연결 정보 
dsn = cx_Oracle.makedsn(host = 'project-db-stu.ddns.net', port = 1524, sid = 'xe')
db = cx_Oracle.connect(user = 'c_team', password = 'c_team123', dsn = dsn)


    
con_ip='project-db-stu.ddns.net:1524/c_team'
con_id='c_team'
con_pw='c_team123'
connection = cx_Oracle.connect(con_id,con_pw, con_ip)

cursor = connection.cursor()

# Flask-Login 확장 설정
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# 회원가입 폼
class JoinForm(FlaskForm):
    user_mail = StringField('Usermail', validators=[DataRequired()])
    user_pw = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Join')

# 로그인 폼
class LoginForm(FlaskForm):
    user_mail = StringField('Username', validators=[DataRequired()])
    user_pw = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

# 회원가입
@app.route('/Join', methods=['GET', 'POST'])
def Join():
    form = JoinForm()
    if form.validate_on_submit():
        # 사용자 정보를 users 테이블에 저장
        user_mail = form.user_mail.data
        uesr_pw = form.user_pw.data
        cursor.execute("INSERT INTO users (user_mail, uesr_pw) VALUES (:user_mail, :uesr_pw)", {"user_mail": user_mail, "uesr_pw": uesr_pw})
        connection.commit()