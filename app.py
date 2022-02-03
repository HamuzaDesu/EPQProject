from flask import Flask, redirect, render_template, request, session, url_for
from auth import auth

app = Flask(__name__)

app.register_blueprint(auth)

app.secret_key = 'TEMP_SECRET_KEY'

@app.route('/')
def index():
    if 'LOGGED_IN' in session:
        if session['LOGGED_IN']:
            return render_template('index.html', firstName = session['user']['firstName'], lastName = session['user']['lastName'])
        else:
            return redirect(url_for('auth.login'))
    else:
        # first time startup on app
        session['LOGGED_IN'] = False
        return redirect('/')

