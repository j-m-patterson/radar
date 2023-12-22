# radar.py
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Create a SQLite database connection and cursor
db_path = 'radar.db'

# inject enumerate
@app.context_processor
def inject_enumerate():
    return dict(enumerate=enumerate)

# Define routes and views
@app.route('/')
def index():
    #connect to db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Fetch partners from the database
    cursor.execute('SELECT * FROM partner')
    partners = cursor.fetchall()
    return render_template('index.html', partners=partners)

@app.route('/settings', methods=['POST','GET'])
def settings():
    #connect to db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if request.method == "POST":
        if "new_partner" in request.form:
            new_partner_name = request.form["new_partner"]
            query = "INSERT into partner (partner_name) VALUES (?)"
            cursor.execute(query, (new_partner_name,))
            conn.commit()
        if "new_agenda_item" in request.form:
            new_item_name = request.form["new_agenda_item"]
            query = "INSERT into agenda_item (item_descr) VALUES (?)"
            cursor.execute(query, (new_item_name,))
            conn.commit()
    # Fetch partners from the database
    cursor.execute('SELECT partner_name FROM partner')
    partners = cursor.fetchall()
    # Fetch agenda_items from the database
    cursor.execute('SELECT item_descr FROM agenda_item')
    agenda_items = cursor.fetchall()
    return render_template('settings.html', partners=partners, agenda_items=agenda_items)

@app.route('/add_check_in', methods=['POST'])
def add_check_in():
    #connect to db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    participant = request.form.get('participant')
    review_checkboxes = request.form.getlist('review_check')
    agenda_checkboxes = request.form.getlist('agenda_check')
    agenda_textboxes = request.form.getlist('agenda_text')
    discuss_textboxes = request.form.getlist('discuss_text')
    action_point_textboxes = request.form.getlist('action_point_text')

    # Save the check-in to the database
    cursor.execute('''
        INSERT INTO check_ins (
            participant, review_checkboxes, agenda_checkboxes, discuss_textboxes, action_point_textboxes
        ) VALUES (?, ?, ?, ?, ?)
    ''', (participant, str(review_checkboxes), str(agenda_checkboxes), str(discuss_textboxes), str(action_point_textboxes)))

    conn.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
