from flask import Blueprint, request, session, flash, redirect, url_for

from utils.classroom import Classroom, get_class
from utils.user import User, get_user
import pprint
from uuid import uuid4

api = Blueprint('api', __name__)

@api.route('/api/createClassroom', methods=['POST'])
def create_classroom():
    classCode = request.form['classCode']
    className = request.form['className']

    if classCode == '' or className == '':
        flash('Please fill in the fields required')
        return redirect(url_for('index.classes'))
    
    if len(Classroom.objects(class_code=classCode)) != 0:
        flash('Classcode already exits')
        return redirect(url_for('index.classes'))

    classRoom = Classroom(
        teacher = session['user']['uuid'],
        class_code = classCode,
        name = className
    ).save()

    teacher = User.objects.get(uuid=session['user']['uuid'])
    teacher.classes.append(Classroom.objects.get(class_code=classCode).class_code)
    teacher.save()

    session['user'] = get_user(session['user']['uuid'])
        
    return redirect(url_for('index.classes'))

@api.route('/api/joinClassroom', methods=['POST'])
def join_classroom():
    classCode = request.form['classCode']

    try:
        if classCode == '': raise Exception 

        student = User.objects.get(uuid=session['user']['uuid'])
        classRoom = Classroom.objects.get(class_code=classCode)
        
        classRoom.students.append(student.uuid)
        classRoom.save()

        student.classes.append(classRoom.class_code)
        student.homeworks[f'{classCode}'] = {'uncompleted': [], 'completed': []}
        student.save()

    except Exception as e:
        flash('Incorrect details. Please try again')
        flash(str(e))
    session['user'] = get_user(session['user']['uuid'])
    return redirect(url_for('index.classes'))

@api.route('/api/get_class_info/<class_code>')
def get_class_info(class_code):
    return get_class(class_code)

@api.route('/api/get_user_info/<uuid>')
def get_user_info(uuid):
    return get_user(uuid)

@api.route('/api/removeStudent/<class_code>/<student_uuid>')
def remove_student(class_code, student_uuid):

    classroom = Classroom.objects.get(class_code=class_code)
    classroom.students.remove(student_uuid)
    classroom.save()

    student = User.objects.get(uuid=student_uuid)
    student.classes.remove(class_code)
    del student.homeworks[f'{class_code}']
    student.save()

    return redirect(url_for('index.class_room', class_code=class_code))

@api.route('/api/setHomework/<class_code>', methods=['POST'])
def set_homework(class_code):
    title = request.form['homeworkTitle']
    description = request.form['homeworkDescription']
    dateDue = request.form['dateDue']

    homework = {
        'id': str(uuid4()),
        'title': title,
        'description': description,
        'dateDue': dateDue
    }

    classroom = Classroom.objects.get(class_code=class_code)
    classroom.homeworks.append(homework)
    classroom.save()

    for uuid in classroom.students:
        student = User.objects.get(uuid=uuid)
        student.homeworks[f'{class_code}']['uncompleted'].append(homework)
        student.save()
        pprint.pprint(student.homeworks)

    flash('Homework set')
    return redirect(url_for('index.class_room', class_code=class_code))

@api.route('/api/setHomeworkComplete/<student_uuid>/<homework_id>/<class_code>')
def set_homework_as_complete(student_uuid, homework_id, class_code):
    student = User.objects.get(uuid=student_uuid)

    for count, homework in enumerate(student.homeworks[f'{class_code}']['uncompleted']):
        if homework['id'] == homework_id:
            student.homeworks[f'{class_code}']['completed'].append(homework)
            student.homeworks[f'{class_code}']['uncompleted'].pop(count)
            student.save()

    return redirect(url_for('index.class_room', class_code=class_code))

@api.route('/api/removeHomeowrk/<class_code>/<homework_id>')
def remove_homework(class_code, homework_id):
    classroom = Classroom.objects.get(class_code=class_code)

    for count, homework in enumerate(classroom.homeworks):
        if homework['id'] == homework_id:
            classroom.homeworks.pop(count)

    for user in classroom.students:
        student = User.objects.get(uuid=user)

        for count, homework in enumerate(student.homeworks[f'{class_code}']['uncompleted']):
            if homework['id'] == homework_id:
                student.homeworks[f'{class_code}']['uncompleted'].pop(count)

    classroom.save()
    student.save()
    
    return redirect(url_for('index.class_room', class_code=class_code))

@api.route('/api/deleteClassroom/<class_code>/<teacher_uuid>')
def delete_class_room(class_code, teacher_uuid):
    classRoom = Classroom.objects.get(class_code=class_code)

    teacher = User.objects.get(uuid=teacher_uuid)
    for count, classroom in enumerate(teacher.classes):
        if classroom ==  class_code:
            teacher.classes.pop(count)

    pprint.pprint(classRoom)

    for user in classRoom.students:
        student = User.objects.get(uuid=user)

        for count, classroom in enumerate(student.classes):
            if classroom == class_code:
                student.classes.pop(count)
        del student.homeworks[f'{class_code}']

        student.save()
    
    classRoom.delete()

    teacher.save()
    classRoom.save()

    return redirect(url_for('index.classes'))
