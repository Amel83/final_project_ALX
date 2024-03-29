# app.py
from flask import Flask, render_template, request, redirect, url_for
import mysql.connector



app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key

def load_user(user_id):
    # Implement a function to load a user from your user database
    pass
# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="T97661122@",
    database="holiday_calendar"
)

cursor = db.cursor()

# Routes
@app.route('/')
def index():
    cursor.execute("SELECT * FROM holidays")
    holidays = cursor.fetchall()
    return render_template('index.html', holidays=holidays)

@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    name = request.form['name']
    date = request.form['date']
    description = request.form['description']
    image_url = request.form['image_url']
    
    cursor.execute("INSERT INTO holidays (name, date, description, image_url) VALUES (%s, %s, %s, %s)",
                   (name, date, description, image_url))
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

if __name__ == '__main__':
    app.run(debug=True)
