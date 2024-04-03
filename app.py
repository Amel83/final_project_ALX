import os
from flask import Flask, session, render_template, request, redirect, url_for
from models import Holiday, User, db
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)
PER_PAGE = 8

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    total_holidays = Holiday.count_holidays()
    offset = (page - 1) * PER_PAGE
    holidays = Holiday.get_holidays(offset)
    return render_template('index.html', holidays=holidays, total_holidays=total_holidays, per_page=PER_PAGE, page=page)

@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    name = request.form['name']
    date = request.form['date']
    description = request.form['description']
    location = request.form['location']
    Holiday.add_holiday(name, date, description, location)
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_holiday(id):
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        location = request.form['location']
        Holiday.edit_holiday(id, name, date, description, location)
        return redirect(url_for('index'))
    else:
        holiday = Holiday.get_holiday_by_id(id)
        return render_template('edit.html', holiday=holiday)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_holiday(id):
    Holiday.delete_holiday(id)
    return redirect(url_for('index'))

@app.route('/like/<int:holiday_id>', methods=['POST'])
def like_holiday(holiday_id):
    if 'username' not in session:
        # Redirect to login page if user is not logged in
        return redirect(url_for('signin'))

    username = session['username']
    user = User.get_user(username)
    user_id = user['id']  # Assuming 'id' is the primary key of the users table

    # Check if the user has already liked the holiday
    cursor = db.cursor()
    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND holiday_id = %s", (user_id, holiday_id))
    if cursor.fetchone():
        # User has already liked this holiday
        return redirect(url_for('index'))

    # If the user hasn't liked the holiday yet, record the like
    cursor.execute("INSERT INTO likes (user_id, holiday_id) VALUES (%s, %s)", (user_id, holiday_id))
    db.commit()
    
    # Increment likes count in the holidays table
    cursor.execute("UPDATE holidays SET likes = likes + 1 WHERE id = %s", (holiday_id,))
    db.commit()

    return redirect(url_for('index'))

@app.route('/share/<int:holiday_id>', methods=['POST'])
def share_holiday(holiday_id):
    # Code to share the holiday (e.g., send an email, post on social media, etc.)
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create_user(username, password)
        return redirect(url_for('index'))
    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            # Handle invalid login
            return render_template('signin.html', error='Invalid username or password')
    return render_template('signin.html')

# app.py

@app.route('/signout')
def signout():
    # Remove user from session
    session.pop('username', None)
    # Redirect to the index page or any other desired page
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
