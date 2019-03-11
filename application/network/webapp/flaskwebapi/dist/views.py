# coding=UTF-8

from flask import Blueprint, request
from flask_restplus import Resource, Api
from flask_restplus import Resource, fields

myapp = Blueprint('api', __name__)
myapi = Api(myapp)

@myapi.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

model = myapi.model('Model', {
    'name': fields.String,
    'address': fields.String,
    'date_updated': fields.DateTime(dt_format='rfc822'),
})

@myapi.route('/todo')
class Todo(Resource):
    @myapi.marshal_with(model, envelope='resource')
    def get(self, **kwargs):
        return db_get_todo()  # Some function that queries the db
