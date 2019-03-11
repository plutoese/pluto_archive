# coding = UTF-8

import sys
import os
sys.path.append(os.getcwd())
print(sys.path)

from flask import Flask
from flask_restful import Api
from dist.views import myapp, HelloWorld, TodoSimple

SECRET_KEY = 'Another random secret key'

app = Flask(__name__)
api = Api(app)
app.register_blueprint(myapp)

api.add_resource(HelloWorld, '/', '/helloworld')
api.add_resource(TodoSimple, '/<string:todo_id>')

app.run(debug=True,use_reloader=False,port=80)