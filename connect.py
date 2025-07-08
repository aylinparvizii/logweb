import mysql.connector

# اتصال به دیتابیس
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="tranport_db"
)

cursor = conn.cursor()

# اجرای کوئری
cursor.execute("SELECT * FROM Passenger")

# گرفتن نتایج
rows = cursor.fetchall()

# چاپ نتایج
for row in rows:
    print(row)

# بستن اتصال
cursor.close()
conn.close()


