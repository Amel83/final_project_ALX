from flask import Flask, render_template, request, redirect, url_for
from models import Holiday
from datetime import datetime

app = Flask(__name__)

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
    Holiday.like_holiday(holiday_id)
    return redirect(url_for('index'))

@app.route('/share/<int:holiday_id>', methods=['POST'])
def share_holiday(holiday_id):
    # Code to share the holiday (e.g., send an email, post on social media, etc.)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
