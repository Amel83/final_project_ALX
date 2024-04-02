import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="T97661122@",
    database="holiday_calendar"
)
PER_PAGE = 8

class User:
    @staticmethod
    def create_user(username, password):
        cursor = db.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        db.commit()

    @staticmethod
    def get_user(username):
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cursor.fetchone()
    
class Holiday:
    @staticmethod
    def get_holidays(offset):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM holidays LIMIT %s OFFSET %s", (PER_PAGE, offset))
        return cursor.fetchall()

    @staticmethod
    def count_holidays():
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM holidays")
        return cursor.fetchone()[0]

    @staticmethod
    def add_holiday(name, date, description, location):
        cursor = db.cursor()
        cursor.execute("INSERT INTO holidays (name, date, description, location) VALUES (%s, %s, %s, %s)",
                       (name, date, description, location))
        db.commit()

    @staticmethod
    def edit_holiday(id, name, date, description, location):
        cursor = db.cursor()
        cursor.execute("UPDATE holidays SET name = %s, date = %s, description = %s, location = %s WHERE id = %s",
                       (name, date, description, location, id))
        db.commit()

    @staticmethod
    def delete_holiday(id):
        cursor = db.cursor()
        cursor.execute("DELETE FROM holidays WHERE id = %s", (id,))
        db.commit()

    @staticmethod
    def like_holiday(holiday_id):
        cursor = db.cursor()
        cursor.execute("SELECT likes FROM holidays WHERE id = %s", (holiday_id,))
        likes = cursor.fetchone()[0]  # Fetch the current likes count
        if likes is None:
            likes = 1
        else:
            likes += 1
        cursor.execute("UPDATE holidays SET likes = %s WHERE id = %s", (likes, holiday_id))
        db.commit()

    @staticmethod
    def get_holiday_by_id(id):
        cursor = db.cursor()
        cursor.execute("SELECT * FROM holidays WHERE id = %s", (id,))
        return cursor.fetchone()
