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
# db연결 함수
def connect():
	#라이브러리 연결
    try :
        cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\smhrd\Oracle\instantclient_21_9")
    
        con_ip='project-db-stu.ddns.net:1524/c_team'
        con_id='c_team'
        con_pw='c_team123'
 
        #db 연결에 필요한 기본 정보(유저, 비밀번호, 데이터베이스 서버 주소)
        connection = cx_Oracle.connect(con_id,con_pw, con_ip)
        print('연결 성공')
        return connection
    except :
        print('연결 실패')
        return None
   
# 종료 
def close():
    try:    
        cursor.close()
        connection.close()
    except : 
        print('close error')



# 회원가입 
def join():
    try : 
        connect()

        cursor = connection.cursor()
        cursor.execute("""insert into c_user(user_mail, user_pw,,user_admin,user_plan,user_joinplan, user_expiration) 
                        values(?,?,'N','A',CURRENT_DATE, CURRENT_DATE+30)""")

        db.commit()
        print("join successfully!")

    except Exception as e: 
        print('join error')
    finally :
        close()


# 로그인을 만들어보장
def login():
    try : 
        user_email = request.form.get("user_email")
        uesr_pw = request.form.get("user_pw")
        connect()

        cursor = connection.cursor()

        cursor.execute("select * from c_user where user_mail =: user_email  and user_pw = user_pw", {"user_email":user_email, "user_pw": uesr_pw})
        user = cursor.fetchall()

        if user[0] == 1 : 
            print('login successfully!')
        else : 
            print('login errorrrr')


    except Exception as e: 
        print('SB login error')
    finally :
        close()





# dsn = cx_Oracle.makedsn('project-db-stu.ddns.net', 1524, 'c_team')
# db = cx_Oracle.connect('c_team', 'c_team123')

# cursor = db.cursor()
# cursor.execute("select * from test_user where user_mail = ?")

# row = cursor.fetchall()
# colname = cursor.description
# col = []

# for i in colname:
#     col.append(i[0])

# #DataFrame으로 불러오기

# df = pd.DataFrame(row, columns = col)

# df=pd.real_sql(""" sql 구문 적기 """ , con = connection)
############################################################################
##############################################################################

# from flask import Flask
# import cx_Oracle

# app = Flask(__name__)

# # Oracle DB 연결 정보
#con_ip='project-db-stu.ddns.net:1524/c_team'
# con_id='c_team'
# con_pw='c_team123'
# connection = cx_Oracle.connect(con_id,con_pw, con_ip)

# # db연결 함수
# def connect_to_oracle():
#     try:
#         # db 연결
#         connection = cx_Oracle.connect(con_id,con_pw, con_ip)
#         print("O연결 성공.")
#         return connection
#     except Exception as e:
#         print("연결 실패:", e)
#         return None

# # 쿼리 실행 함수
# def execute_query(query):
#     connection = connect_to_oracle()

#     if connection:
#         cursor = connection.cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
#         connection.close()
#         return result

#     else:
#         return None

# # 쿼리
# @app.route("/")
# def home():
#     query = "select * from c_user where user_mail =: user_email  and user_pw = user_pw", {"user_email":user_email, "user_pw": uesr_pw}"
#     result = execute_query(query)
#     return str(result)

# if __name__ == "__main__":
#     app.run()
