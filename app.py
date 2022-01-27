from flask import Flask, redirect, render_template, request, session

app = Flask(__name__)

app.secret_key = 'TEMP_SECRET_KEY'

@app.route('/')
def index():
    return render_template('index.html', username = session['user']['username'])

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/auth/login.html')
    else:
        for item in request.form:
            print(request.form[item])

        session['user'] = {
            'username': request.form['username']
        }

        return redirect('/')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('/auth/register.html')
    else:
        # register account logic here
        for item in request.form:
            print(request.form[item])
        return redirect('/login')
        