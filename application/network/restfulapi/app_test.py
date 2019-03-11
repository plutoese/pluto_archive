# coding = UTF-8

from requests import put, get

put('http://localhost/todo1', data={'data': 'Remember the milk'})
