import pymysql

db = pymysql.connect('localhost', 'root', 'Lichang1-', 'django_mysql')
cursor = db.cursor()
cursor.execute('select * from django_mysql.mhuser_mhuser')
result = cursor.fetchall()
print(result)