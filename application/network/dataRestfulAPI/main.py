# coding = UTF-8

import sys
import os
sys.path.append(os.getcwd())
print(sys.path)

from flask import Flask
from apis import api

app = Flask(__name__)
api.init_app(app)

if __name__ == '__main__':
    app.run(debug=True, port=80)