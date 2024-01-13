# radar.py
import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Create a SQLite database connection and cursor
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(ROOT_DIR, 'radar.db')

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
    cursor.close()
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
    cursor.close()
    return render_template('settings.html', partners=partners, agenda_items=agenda_items)

@app.route('/review', methods=['POST'])
def review():
    #connect to db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    #calculate partner bitmap INT
    partner_bitmap = 0
    for partner_id in request.form["partner_check"]:
        partner_bitmap += 2**int(partner_id)
    #get list of check-ins for this partner bitmap
    query = 'SELECT * from check_in WHERE partner_id_bitmap = ?'
    cursor.execute(query, (partner_bitmap,))
    check_ins = cursor.fetchall()
    #get list of unresolved action points from those check-ins
    checkinlist = []
    for item in check_ins:
        checkinlist.append(item[0])
    query = "select * from discuss_action_points where is_resolved = FALSE and check_in_id in (%s)" % ",".join(map(str,checkinlist))
    cursor.execute(query)
    action_points = cursor.fetchall()
    cursor.close()
    return render_template('review.html', action_points=action_points, check_ins=check_ins)

@app.route('/agenda', methods=['POST'])
def agenda():
    #connect to db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Fetch agenda_items from the database
    cursor.execute('SELECT * FROM agenda_item')
    agenda_items = cursor.fetchall()
    cursor.close()
    return render_template('agenda.html', agenda_items=agenda_items)

@app.route('/discuss', methods=['POST'])
def discuss():
    #connect to db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    #list discussions and action points from the current check_in
    cursor.close()
    return render_template('discuss.html')

@app.route('/view_check_in', methods=['GET'])
def view_check_in():
    #connect to db
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.close()
    return render_template('view_check_in.html')

if __name__ == '__main__':
    app.run(debug=True)
