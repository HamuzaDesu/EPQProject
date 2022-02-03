from flask import Blueprint, flash, request, redirect, render_template, session, url_for
from pymongo import MongoClient
import hashlib

auth = Blueprint('auth', __name__)

mongoUrl = 'mongodb://localhost:27017/'

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/auth/login.html')
    else:
        username = request.form['username']
        # hash password
        password = hashlib.sha256(request.form['password'].encode('utf-8')).hexdigest()
        
        with MongoClient(mongoUrl) as client:
            db = client.EPQProject
            users = db.users

            user = users.find_one({'username': username})

            if user:
                if password == user['password']:
                    session['LOGGED_IN'] = True

                    session['user'] = {
                        'username': user['username'],
                        'firstName': user['firstName'],
                        'lastName': user['lastName']
                    }
                else:
                    flash('Password incorrect')
                    return redirect(url_for('.login'))
            else:
                flash('Invalid Credentials. Please try again')
                return redirect(url_for('.login'))

        return redirect(url_for('index'))

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('/auth/register.html')
    else:
        # register account logic here
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        if firstName == '' or lastName == '' or username == '' or password == '':
            flash('Please fill in all required fields.')
            return redirect(url_for('.register'))

        with MongoClient(mongoUrl) as client:
            db = client.EPQProject
            users = db.users

            if users.find_one({'username': username}):
                flash('Username already exists. Please try again')
                return redirect(url_for('.register'))

            users.insert_one({
                'firstName' : firstName,
                'lastName' : lastName,
                'username' : username,
                'password' : hashlib.sha256(password).hexdigest()
            })

        return redirect(url_for('.login'))
