from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import socket, os, asyncio, zipfile
from functools import wraps
from tqdm import tqdm
import user, file2, lda_model2

def async_action(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapped

app = Flask(__name__)
app.secret_key = 'qwer1234'

# 웹에서 requiry.html 호출 시 실행 함수 
@app.route('/requiry', methods = ['GET','POST'])
def requiry():
    return render_template('requiry.html')

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



# async def upload():
#     file_list = request.files.getlist("filename[]") # 업로드된 파일을 리스트 형식으로 변수에 저장
#     user_seq = session['user_info'][0] # 세션에 저장된 c_user 테이블의 user_seq 컬럼에 접근

#     await file2.upload(user_seq, file_list)
#     file_topic = await lda_model2.classification(user_seq)
#     for i in range(len(file_topic)):
#         file_path = f'./uploads/{user_seq}/{file_topic[i]}/'
#         file_name, file_ext = os.path.splitext(file_list[i])
#         await file2.db_update(user_seq, file_path, file_name[i], file_ext)



# 기본 시작페이지    
@app.route('/')
def default():
    return redirect(url_for('main'))

# 웹에서 /main이 호출되면 실행되는 함수 
@app.route('/main', methods = ['GET','POST']) # get, post
@async_action
async def main():
    if request.method == 'POST': # post 방식일때
        # request.files
        file_list = request.files.getlist("filename[]") # 업로드된 파일을 리스트 형식으로 변수에 저장
        user_seq = session['user_info'][0] # 세션에 저장된 c_user 테이블의 user_seq 컬럼에 접근

        await file2.upload(user_seq, file_list) # 파일 업로드
        file_topic = await lda_model2.classification(user_seq) # 업로드된 파일 모델 분류후 file_topic 변수에 저장
        file_list = os.listdir(f'./uploads/{user_seq}/')
        print(file_list)
        file2.db_update(user_seq, file_list, file_topic)
        file2.replace_file(user_seq, file_list, file_topic)
        return redirect(url_for('drive')) # 메인 페이지로 이동
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
            print("회원가입에 실패했습니다.")
            return redirect(url_for('join')) # join 호출
        
    else: # get 방식
        return render_template('join.html') # 회원가입으로 페이지 이동
    
# 웹에서 mypage 호출 시 실행 함수
@app.route('/mypage', methods = ['GET','POST'])
def mypage(): # 메인 페이지
    if request.method == 'POST':
        id = request.form['id']
        pw = request.form['pw']
        pw_c = request.form['pw_c']
        result = False

        if pw == pw_c:
            result = user.modify(id, pw)
            print('result :', result)

        if result: # 정보수정 성공
            print('회원정보를 수정하였습니다.')
            # return render_template('mypage.html', user_id = session['user_info'][0])
            return redirect(url_for('mypage'))
        
        else: # 정보수정 실패
            print('회원정보 수정에 실패했습니다.')
            flash("비밀번호를 확인해주세요.")
            # return render_template('mypage.html', user_id = session['user_info'][0]) # 로그인 페이지로 이동
            return redirect(url_for('mypage'))
    
    else:
        return render_template('mypage.html', user_id = session['user_info'][0], price_type = session['user_info'][1], user_expiration = session['user_info'][3])

# 구독 취소
@app.route('/price_cancel', methods = ['GET','POST'])
def price_cancel(): # 메인 페이지
    if request.method == 'POST':
        id = session['user_info'][0]
        result = user.price_cancel(id)
        print('result :', result)

        if result: # 정보수정 성공
            print('구독을 취소하였습니다.')
            flash("구독을 취소하였습니다.")
            # return render_template('mypage.html', user_id = session['user_info'][0])
            session['user_info'] = result # session 저장
            return redirect(url_for('price_cancel'))
        
        else: # 정보수정 실패
            print('구독취소에 실패하였습니다')
            flash("구독취소에 실패하였습니다.")
            # return render_template('mypage.html', user_id = session['user_info'][0]) # 로그인 페이지로 이동
            return redirect(url_for('price_cancel'))
    
    else:
        return render_template('mypage.html', user_id = session['user_info'][0], price_type = session['user_info'][1], user_expiration = session['user_info'][3])


# 웹에서 drive 호출 시 실행 함수 
@app.route('/drive')
def drive():
    id = session['user_info'][0]
    file_path = f'./uploads/{id}/'
    # file_list = os.listdir(file_path)
    file_list = file2.file_list_in_dir(file_path)
    sum_file_size = 0
    print(file_list)
    if len(file_list)>0:
        for i in range(len(file_list)):
            file_size = os.path.getsize(file_path+file_list[i])
            sum_file_size += file_size
    convert_file_size = file2.convert_size(sum_file_size)
    print('File Size:', convert_file_size, 'bytes')
    return render_template('drive.html')

# 파일 압축 다운로드 
@app.route('/download')
def download():
    user_id = session['user_info'][0]
    # 압축할 폴더 경로
    folder_path = f'./uploads/{user_id}'

    # 압축 파일 생성
    zip_path = f"{folder_path}.zip"
    with zipfile.ZipFile(zip_path, 'w') as zip:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zip.write(os.path.join(root, file))

    # 압축 파일 다운로드
    return send_file(zip_path, as_attachment=True) # 첨부 파일로 다운로드 as_attachment=True

if __name__ == '__main__':
    app.run(host = socket.gethostbyname(socket.gethostname()), port="9999")

