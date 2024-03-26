from flask import render_template, request, redirect, url_for
from app import app, db
from app.models import NamedDay
from datetime import date

@app.route('/')
def index():
    named_days = NamedDay.query.all()
    return render_template('index.html', named_days=named_days)

@app.route('/add_named_day', methods=['POST'])
def add_named_day():
    name = request.form['name']
    date_str = request.form['date']
    date_obj = date.fromisoformat(date_str)
    new_named_day = NamedDay(name=name, date=date_obj)
    db.session.add(new_named_day)
    db.session.commit()
    return redirect(url_for('index'))
