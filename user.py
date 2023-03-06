#app.config['db_connection'] = con

def join(id, pw):
    import cx_Oracle
    
    if not cx_Oracle.init_oracle_client:
        cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\smhrd\Oracle\instantclient_21_9")
    con = cx_Oracle.connect("c_team", "c_team123", "project-db-stu.ddns.net:1524/xe", encoding="UTF-8")
    cursor = con.cursor()
    result = 0
    
    try:
        user_admin = 'N'
        price_type = 'A'

        cursor.execute("INSERT INTO c_user(user_mail, user_pw, user_admin, price_type) VALUES (:1, :2, :3, :4)", [id, pw, user_admin, price_type])
        con.commit()

        result = 1
    except:
        result = 0
    finally:
        cursor.close()
        con.close()
        
    return result
