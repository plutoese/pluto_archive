# coding = UTF-8

from flask import Flask
from flask_script import Manager
from flask_script import Command


class Hello(Command):
    def run(self):
        print("hello world")


app = Flask(__name__)
# configure your app

manager = Manager(app)

manager.add_command('hello', Hello())

if __name__ == "__main__":
    manager.run()
