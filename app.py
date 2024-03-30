# app.py
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="T97661122@",
    database="holiday_calendar"
)

cursor = db.cursor()
PER_PAGE = 5 
def get_holidays(offset):
    cursor.execute("SELECT * FROM holidays LIMIT %s OFFSET %s", (PER_PAGE, offset))
    return cursor.fetchall()

def count_holidays():
    cursor.execute("SELECT COUNT(*) FROM holidays")
    return cursor.fetchone()[0]

def get_marked_dates():
    cursor.execute("SELECT date, name FROM holidays")
    marked_dates = cursor.fetchall()
    return {datetime.strftime(date, "%Y-%m-%d"): name for date, name in marked_dates}


@app.route('/')
def index():
    
    page = request.args.get('page', 1, type=int)
    total_holidays = count_holidays()
    offset = (page - 1) * PER_PAGE
    holidays = get_holidays(offset)
    marked_dates = get_marked_dates()
    current_date = datetime.now() 
    return render_template('index.html', holidays=holidays, total_holidays=total_holidays, per_page=PER_PAGE, marked_dates=marked_dates, current_date=current_date, page=page)
@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    name = request.form['name']
    date = request.form['date']
    description = request.form['description']
       
    cursor.execute("INSERT INTO holidays (name, date, description) VALUES (%s, %s, %s)",
                   (name, date, description))
    db.commit()
    
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_holiday(id):
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        
        # Update the holiday entry in the database
        cursor.execute("UPDATE holidays SET name = %s, date = %s, description = %s WHERE id = %s",
                       (name, date, description, id))
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
    cursor.execute("UPDATE holidays SET likes = likes + 1 WHERE id = %s", (holiday_id,))
    db.commit()
    return redirect(url_for('index'))

@app.route('/share/<int:holiday_id>', methods=['POST'])
def share_holiday(holiday_id):
    # Code to share the holiday (e.g., send an email, post on social media, etc.)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
