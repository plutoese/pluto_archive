# coding=UTF-8

from flask import Blueprint, request
from flask_restful import Resource

myapp = Blueprint('myapp', __name__)

class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

todos = {}

class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}
