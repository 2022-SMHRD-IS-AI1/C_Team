import cx_Oracle

if not cx_Oracle.init_oracle_client:
    cx_Oracle.init_oracle_client(lib_dir=r".\Oracle\instantclient_21_9")

# db 연결
def connect():
    return cx_Oracle.connect("c_team", "c_team123", "project-db-stu.ddns.net:1524/xe", encoding="UTF-8")
    
# 회원가입
def join(id, pw):
    con = connect() # db 연결
    cursor = con.cursor() # cursor 객체(튜플) 생성
    try: 
        user_admin = 'N' # 관리자 여부 : N (일반회원)
        price_type = 'Basic' # 기본 플랜 (Basic, Pro, Custom)
        # sql문
        sql = "INSERT INTO c_user(user_mail, user_pw, user_admin, price_type) VALUES(:1, :2, :3, :4)"
        cursor.execute(sql, [id, pw, user_admin, price_type]) # sql문 실행
        con.commit() # 커밋
        result = True # result에 성공여부 초기화 (True : 성공)

    except Exception as e: # 예외 처리
        print(e) # 예외 메시지 출력
        result = False # result에 성공여부 초기화 (False : 실패)

    finally: # 예외 여부와 관계없이 실행
        cursor.close() # cursor 객체 닫기
        con.close() # db 연결 닫기

    return result # result(성공여부) 리턴


# 로그인
def login(id, pw):
    con = connect() # db 연결
    cursor = con.cursor() # cursor 객체(튜플) 생성
    result = [] # result를 list 형태로 생성
    try:
        # sql문
        sql = "SELECT user_mail, price_type, user_joinprice, user_expiration FROM c_user WHERE user_mail = :1 AND user_pw = :2"
        cursor.execute(sql, [id, pw]) # sql문 실행
        data = cursor.fetchone() # data에 sql문 결과(1행) 저장
        if data:
            result = list(data) # result에 data를 리스트 형태로 저장

    except Exception as e: # 예외 처리
        print(e) # 예외 메시지 출력

    finally: # 예외 여부와 관계없이 실행
        cursor.close() # cursor 객체 닫기
        con.close() # db 연결 닫기

    return result # result(세션에 저장할 리스트 형태의 data) 리턴

# 회원정보 수정
def modify(id, pw):
    con = connect() # db 연결
    cursor = con.cursor() # cursor 객체(튜플) 생성
    try:
        # sql문
        sql = "UPDATE c_user SET user_pw = :1 WHERE user_mail = :2"
        cursor.execute(sql, [pw, id]) # sql문 실행
        con.commit() # 커밋
        result = True # result에 성공여부 초기화 (True : 성공)

    except Exception as e:
        print(e) # 예외 메시지 출력
        result = False # result에 성공여부 초기화 (False : 실패)

    finally: # 예외 여부와 관계없이 실행
        cursor.close() # cursor 객체 닫기
        con.close() # db 연결 닫기

    return result # result(성공여부) 리턴

# 구독 취소
def price_cancel(id):
    con = connect() # db 연결
    cursor = con.cursor() # cursor 객체(튜플) 생성
    result = [] # result를 list 형태로 생성
    try:
        # sql문
        sql = "UPDATE c_user SET price_type = 'Basic' WHERE user_mail = :1"
        cursor.execute(sql, [id]) # sql문 실행
        con.commit() # 커밋
        sql = "SELECT user_mail, price_type, user_joinprice, user_expiration FROM c_user WHERE user_mail = :1"
        cursor.execute(sql, [id]) # sql문 실행
        data = cursor.fetchone() # data에 sql문 결과(1행) 저장
        if data:
            result = list(data) # result에 data를 리스트 형태로 저장

    except Exception as e:
        print(e) # 예외 메시지 출력

    finally: # 예외 여부와 관계없이 실행
        cursor.close() # cursor 객체 닫기
        con.close() # db 연결 닫기

    return result # result(세션에 저장할 리스트 형태의 data) 리턴