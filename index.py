from flask import Blueprint, session, url_for, redirect, render_template, request, flash
from utils.classroom import Classroom, get_class
from utils.user import User, get_user

index = Blueprint('index', __name__)

@index.route('/')
def root():
    if 'LOGGED_IN' not in session:
        session['LOGGED_IN'] = False

    if not session['LOGGED_IN']:
        return redirect(url_for('auth.login'))

    session['user'] = get_user(session['user']['uuid']) # refresh session

    return render_template('index/home.html', user=session['user'])



@index.route('/classes')
def classes():
    session['user'] = get_user(session['user']['uuid']) # refresh session
    return render_template('index/classes.html', user=session['user'])

@index.route('/classroom/<class_code>')
def class_room(class_code):
    session['user'] = get_user(session['user']['uuid']) # refresh session

    classroom = get_class(class_code)
    return render_template('index/classroom.html', user=session['user'], classroom=classroom)


