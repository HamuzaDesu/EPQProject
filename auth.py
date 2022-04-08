from pprint import pprint
import uuid
from flask import Blueprint, flash, request, redirect, render_template, session, url_for
import hashlib

from utils.user import User, get_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('/auth/login.html')

    username = request.form['username'].strip()
    password = hashlib.sha256(request.form['password'].encode('utf-8').strip()).hexdigest() # hashes password

    try:
        user = User.objects.get(username=username)
        pprint(user)

        if user.password != password:
            raise Exception

        session['LOGGED_IN'] = True
        session['user'] = get_user(user.uuid)

        return redirect(url_for('index.root'))

    except:
        flash('Incorrect details. Please try again')
        return redirect(url_for('.login'))
        

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index.root'))

@auth.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        return render_template('/auth/register.html')
    else:
        # register account logic here
        username = request.form['username'].strip()
        firstName = request.form['firstname'].strip()
        lastName = request.form['lastname'].strip()
        password = hashlib.sha256(request.form['password'].encode('utf-8').strip()).hexdigest()
        isTeacher = True if request.form['isTeacher'] == 'True' else False

        if firstName == '' or lastName == '' or username == '' or password == '':
            flash('Please fill in all required fields.')
            return redirect(url_for('.register'))

        if len(User.objects(username=username)) != 0:
            flash('Username already exists')
            return redirect(url_for('.register'))

        user = User(
            uuid = str(uuid.uuid4()),
            username = username,
            password = password,
            first_name = firstName,
            last_name = lastName,
            is_teacher = isTeacher
        ).save()

        return redirect(url_for('.login'))
