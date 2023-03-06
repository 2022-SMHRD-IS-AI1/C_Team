import cx_Oracle
from flask import Flask, session, render_template, redirect, request, url_for

app = Flask(__name__)
app.secret_key = 'qwer1234'

cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\smhrd\Oracle\instantclient_21_9")
con = cx_Oracle.connect("c_team", "c_team123", "project-db-stu.ddns.net:1524/xe", encoding="UTF-8")
cursor = con.cursor()


app.config['db_connection'] = con



def register():
    

    if request.method == 'POST':
      
        id = request.form['id'] 
        pw = request.form['pw']
        user_admin = 'N'
        price_type = 'A'
       
        cursor = con.cursor()
 
        cursor.execute("INSERT INTO c_user(user_mail, user_pw, user_admin, price_type) VALUES (:1, :2,:3,:4)",[id,pw,user_admin,price_type])
        con.commit()   
 
        cursor.close()
        con.close()
        return render_template('Main.html')
    return render_template('join.html')