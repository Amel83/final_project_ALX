import os
from flask import Flask, session, render_template, request, redirect, url_for
from models import Holiday, User, db
from datetime import datetime
from flask import flash


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_TYPE'] = 'filesystem'  # or any other session type you prefer

PER_PAGE = 8

"""
Route for the homepage, displaying a list of holidays.
"""
@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    total_holidays = Holiday.count_holidays()
    offset = (page - 1) * PER_PAGE
    holidays = Holiday.get_holidays(offset)
    return render_template('index.html', holidays=holidays, total_holidays=total_holidays, per_page=PER_PAGE, page=page)

"""
Route to add a new holiday.
"""
@app.route('/add_holiday', methods=['POST'])
def add_holiday():
    if 'username' not in session:
        return redirect(url_for('signin'))
    name = request.form['name']
    date = request.form['date']
    description = request.form['description']
    location = request.form['location']

    username = session['username']
    user = User.get_user(username)
    user_id = user['id']

    Holiday.add_holiday(name, date, description, location, user_id)
    return redirect(url_for('index'))

"""
Route to edit an existing holiday.
"""
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_holiday(id):
    if 'username' not in session:
        return redirect(url_for('signin'))

    # Get the logged-in user's ID
    username = session['username']
    user = User.get_user(username)
    user_id = user['id']

    # Check if the holiday belongs to the logged-in user
    holiday = Holiday.get_holiday_by_id(id)
    if holiday[7] != user_id:
        flash("You can only edit your own holiday posts.")
        return redirect(url_for('index'))
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        description = request.form['description']
        location = request.form['location']
        Holiday.edit_holiday(id, name, date, description, location)
        flash("holiday post edited", "info")
        return redirect(url_for('index'))
    else:
        holiday = Holiday.get_holiday_by_id(id)
        return render_template('edit.html', holiday=holiday)

"""
Route to delete a holiday.
"""
@app.route('/delete/<int:id>', methods=['POST'])
def delete_holiday(id):
    if 'username' not in session:
        return redirect(url_for('signin'))

    # Get the logged-in user's ID
    username = session['username']
    user = User.get_user(username)
    user_id = user['id']

    holiday = Holiday.get_holiday_by_id(id)
    if holiday[7] != user_id:
        flash("You can only delete your own holiday posts.")
        return redirect(url_for('index'))
    Holiday.delete_holiday(id)
    return redirect(url_for('index'))

"""
Route to like a holiday.
"""
@app.route('/like/<int:holiday_id>', methods=['POST'])
def like_holiday(holiday_id):
    if 'username' not in session:
        flash("You need to sign in to like a holiday.")
        return redirect(url_for('signin'))

    username = session['username']
    user = User.get_user(username)
    user_id = user['id']  
    # Check if the user has already liked the holiday
    cursor = db.cursor()
    cursor.execute("SELECT * FROM likes WHERE user_id = %s AND holiday_id = %s", (user_id, holiday_id))
    if cursor.fetchone():
        flash("You have already liked this holiday.")
        return redirect(url_for('index'))

    cursor.execute("INSERT INTO likes (user_id, holiday_id) VALUES (%s, %s)", (user_id, holiday_id))
    db.commit()
    
    cursor.execute("UPDATE holidays SET likes = likes + 1 WHERE id = %s", (holiday_id,))
    db.commit()
    Holiday.like_holiday(holiday_id) 
    return redirect(url_for('index'))

"""
Route for user signup.
"""
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        User.create_user(username, password)
        flash("created account sucessfully", "info")
        return redirect(url_for('index'))
    return render_template('signup.html')

"""
Route for user signin.
"""
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.get_user(username)
        if user and user['password'] == password:
            session['username'] = username
            flash("logeged in sucessful", "info")
            return redirect(url_for('index'))
        else:
            # Handle invalid login
            return render_template('signin.html', error='Invalid username or password')
    return render_template('signin.html')

@app.route('/signout')
def signout():
   
    session.pop('username', None)
    return redirect(url_for('index'))

"""
Adding an about page
"""
@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=False)
