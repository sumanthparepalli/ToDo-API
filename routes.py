from datetime import datetime

from flask import request, jsonify, session
from flask_login import login_user, login_required, logout_user
from sqlalchemy import desc, Date

from app import app, login, db
from models import *


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/app/agent', methods=['POST'])
def signUp():
    username = request.json['agent_id']
    password = request.json['password']
    if db.session.query(User).filter(User.username == username).first() is not None:
        res = {
            'status': 'Agent Id exists',
            'status_code': 424
        }
        return jsonify(res), 200
    new_user = User(username=username)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    res = {
        'status': 'account created',
        'status_code': 200
    }
    return jsonify(res), 200


@app.route('/app/agent/auth', methods=['POST'])
def login():
    username = request.json['agent_id']
    password = request.json['password']
    user = db.session.query(User).filter(User.username == username).first()
    if user is None or not user.check_password(password):
        res = {
            'status': 'failure',
            'status_code': 401
        }
        return jsonify(res)
    else:
        res = {
            'status': 'success',
            'agent_id': user.id,
            'status_code': 200
        }
        login_user(user, remember=False)
        return res


@app.route('/app/sites/list', methods=['get'])
@login_required
def list_todo():
    id = request.args.get('agent')
    return jsonify(
        [i.getJson() for i in db.session.query(Todo).filter(Todo.userId == id).order_by(Todo.due_date).all()])


@app.route('/app/sites/', methods=['POST', 'GET'])
@login_required
def saveTodo():
    title = request.json['title']
    description = request.json['description']
    category = request.json['category']
    due_date = request.json['due_date']
    id = request.args.get('agent')
    due_date = datetime.strptime(due_date, '%Y-%m-%d')
    todo = Todo(title=title,
                description=description,
                category=category,
                due_date=due_date,
                userId=id)
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        'status': 'success',
        'status_code': 200
    }), 200


@app.route('/app/logout')
def logout():
    session.clear()
    logout_user()
    return jsonify({
        'status': 'logged out',
        'status_code': '200'
    })
