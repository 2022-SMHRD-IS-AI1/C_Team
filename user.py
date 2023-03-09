import cx_Oracle

# Initialize Oracle client
if not cx_Oracle.init_oracle_client:
    cx_Oracle.init_oracle_client(lib_dir=r".\Oracle\instantclient_21_9")

# db접속
def connect():
    return cx_Oracle.connect("c_team", "c_team123", "project-db-stu.ddns.net:1524/xe", encoding="UTF-8")

# 회원가입
def join(id, pw):
    con = connect()
    cursor = con.cursor()
    try:
        user_admin = 'N'
        price_type = 'A'
        sql = "INSERT INTO c_user(user_mail, user_pw, user_admin, price_type) VALUES(:1, :2, :3, :4)"
        cursor.execute(sql, [id, pw, user_admin, price_type])
        con.commit()
        result = True

    except Exception as e:
        print(e)
        result = False

    finally:
        cursor.close()
        con.close()

    return result


# 로그인
def login(id, pw):
    con = connect()
    cursor = con.cursor()
    result = []
    try:
        sql = "SELECT user_mail, price_type, user_joinprice, user_expiration FROM c_user WHERE user_mail = :1 AND user_pw = :2"
        cursor.execute(sql, [id, pw])
        data = cursor.fetchone()
        if data:
            result = list(data)

    except Exception as e:
        print(e)

    finally:
        cursor.close()
        con.close()

    return result

# 회원정보 수정
def modify(id, pw):
    con = connect()
    cursor = con.cursor()
    try:
        sql = "UPDATE c_user SET user_pw = :1 WHERE user_mail = :2"
        cursor.execute(sql, [pw, id])
        con.commit()
        result = True

    except Exception as e:
        print(e)
        result = False

    finally:
        cursor.close()
        con.close()

    return result