from flask import Flask, jsonify, request, url_for, redirect, session

app = Flask(__name__)

app.config['DEBUG'] = True
# Configuring a cookie with a secret key prevents malicious hackers from decoding a cookie and sending it back.
app.config['SECRET_KEY'] = 'ThisIsASecret!'

@app.route('/')
def index():
    return '<h1>Hello, world!</h1>'


@app.route('/home', methods=['POST', 'GET'], defaults={'name': 'Default'})
@app.route('/home/<string:name>', methods=['POST', 'GET'])
def home(name):
    session['name'] = name
    return '<h1>Hello {}, you are on the home page!</h1>'.format(name)


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
        return '''<form method="POST" action="/theform">
        <input type="text" name="name">
        <input type="text" name="location">
        <input type="submit" valur="Submit">
        </form>'''

    else:
        name = request.form['name']
        location = request.form['location']

        # return '<h1>Hello {}. You are from {}. You have submitted the form successfully!<h1>'.format(name, location)
        return redirect((url_for('home', name=name, location=location)))


@app.route('/processjson', methods=['POST'])
def processjson():

    data = request.get_json()

    name = data['name']
    location = data['location']

    randomlist = data['randomlist']

    return jsonify({'result': 'Success!', 'name': name, 'location': location, 'randomkeylist': randomlist[1]})


if __name__ == '__main__':
    app.run()
