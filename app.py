# app.py
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime


app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="T97661122@",
    database="holiday_calendar"
)

cursor = db.cursor()
PER_PAGE = 8
def get_holidays(offset):
    cursor.execute("SELECT * FROM holidays LIMIT %s OFFSET %s", (PER_PAGE, offset))
    return cursor.fetchall()

def count_holidays():
    cursor.execute("SELECT COUNT(*) FROM holidays")
    return cursor.fetchone()[0]

@app.route('/')
def index():
    
    page = request.args.get('page', 1, type=int)
    total_holidays = count_holidays()
    offset = (page - 1) * PER_PAGE
    holidays = get_holidays(offset)
    return render_template('index.html', holidays=holidays, total_holidays=total_holidays, per_page=PER_PAGE, page=page)
@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    name = request.form['name']
    date = request.form['date']
    description = request.form['description']
    location = request.form['location']
    cursor.execute("INSERT INTO holidays (name, date, description, location) VALUES (%s, %s, %s, %s)",
                   (name, date, description, location))
    db.commit()
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_holiday(id):
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        location = request.form['location']
        # Update the holiday entry in the database
        cursor.execute("UPDATE holidays SET name = %s, date = %s, description = %s, location = %s, WHERE id = %s",
                       (name, date, description, location, id))
        db.commit()
        
        return redirect(url_for('index'))
    else:
        # Fetch the holiday entry to be edited from the database
        cursor.execute("SELECT * FROM holidays WHERE id = %s", (id,))
        holiday = cursor.fetchone()
        return render_template('edit.html', holiday=holiday)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_holiday(id):
    # Delete the holiday entry from the database
    cursor.execute("DELETE FROM holidays WHERE id = %s", (id,))
    db.commit()
    
    return redirect(url_for('index'))

@app.route('/like/<int:holiday_id>', methods=['POST'])
def like_holiday(holiday_id):
    cursor.execute("SELECT likes FROM holidays WHERE id = %s", (holiday_id,))
    likes = cursor.fetchone()[0]  # Fetch the current likes count

    if likes is None:  # If likes is NULL, set it to 1
        likes = 1
    else:  # If likes is not NULL, increment it by 1
        likes += 1

    cursor.execute("UPDATE holidays SET likes = %s WHERE id = %s", (likes, holiday_id))
    db.commit()

    return redirect(url_for('index'))


@app.route('/share/<int:holiday_id>', methods=['POST'])
def share_holiday(holiday_id):
    # Code to share the holiday (e.g., send an email, post on social media, etc.)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
