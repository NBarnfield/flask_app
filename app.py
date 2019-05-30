from flask import Flask, jsonify, request, url_for, redirect, session, render_template, g
import sqlite3

app = Flask(__name__)

app.config['DEBUG'] = True
# Configuring a cookie with a secret key prevents malicious hackers from decoding a cookie and sending it back.
app.config['SECRET_KEY'] = 'ThisIsASecret!'


# Connect to the sqlite database in the directory
def connect_db():
    sql = sqlite3.connect("C:\\Users\\Ned Barnfield\\PycharmProjects\\first_application\\data.db")
    # The row_factory method returns results as dictionaries instead of the default tuples.
    sql.row_factory = sqlite3.Row
    return sql


def get_db():
    # g is a global variable used to store the sqlite database.
    # The attribute check is used to ensure that it is connected
    if not hasattr(g, 'sqlite3'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Teardown is automatically called once the route returns.
# This is used here to automatically close the connection to the db once the information has been returned.
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return '<h1>Hello, world!</h1>'


@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    db = get_db()
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()

    return render_template('home.html', name=name, display=True,
                           mylist=['one', 'two', 'three', 'four'], listofdictionaries=[{'name' : 'Zach'}, {'name': 'Zoe'}], results=results)


@app.route('/json')
def json():
    # Adding in an if statement catches the missing name if it is removed rather than returning a keyerror
    if name in session:
        name = session['name']
    else:
        name = 'NonInSession!'
    return jsonify({'key': 'value', 'listkey': [1, 2, 3], 'name': name})


@app.route('/query')
def query():
    name = request.args.get('name')
    location = request.args.get('location')
    return '<h1>Hi {}. You are from {}. You are on the query page!</h1>'.format(name, location)


@app.route('/theform', methods=['POST', 'GET'])
def theform():

    if request.method == 'GET':
        return render_template('form.html')

    else:
        name = request.form['name']
        location = request.form['location']

        db = get_db()
        # Using ? prevents SQL injection. Sqlite will format the insert for you rather .
        db.execute('insert into users (name, location) values (?, ?)', [name, location])
        db.commit()

        # return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, location)
        return redirect((url_for('home', name=name, location=location)))


@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']

    randomlist = data['randomlist']

    return jsonify({'result': 'Success!', 'name': name, 'location': location, 'randomkeylist': randomlist[1]})


@app.route('/viewresults')
def viewresults():
    # Connect to the database and pass in a SQL query
    db = get_db()
    # Cursor is a pointer to the results
    cur = db.execute('select id, name, location from users')
    results = cur.fetchall()
    return '<h1>The ID is {}. The name is {}. ' \
           'The location is {}.</h1>'.format(results[2]['id'], results[2]['name'], results[2]['location'])

if __name__ == '__main__':
    app.run()
