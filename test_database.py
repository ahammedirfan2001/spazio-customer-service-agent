from database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("SELECT COUNT(*) FROM restaurant_info")
info_count = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM menu")
menu_count = cursor.fetchone()[0]

print("Restaurant information records:", info_count)
print("Menu records:", menu_count)

connection.close()