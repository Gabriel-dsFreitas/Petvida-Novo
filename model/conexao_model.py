import mysql.connector as sql

conexao = sql.connect(
    host="tini.click",
    port=3306,
    user="petvida_db",
    password="4287816f7bc22c82a83f70ad492266db",   
    database="petvida_db"
)

cursor = conexao.cursor(dictionary=True)