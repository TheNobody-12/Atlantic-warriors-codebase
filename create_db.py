import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="Sarthak*2512",port = "3306",auth_plugin='mysql_native_password'
)

cursor = mydb.cursor()

cursor.execute("CREATE DATABASE mydatabase")

cursor.execute("SHOW DATABASES")
for db in cursor:
    print(db)


