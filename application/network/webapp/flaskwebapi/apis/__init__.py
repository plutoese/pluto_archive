# coding = UTF-8

from flask_restplus import Api

from .demoAPI import api as ns1

api = Api(
    title='CityStatistics',
    author = 'Glen',
    version='1.0',
    description='中国城市统计年鉴',
)

api.add_namespace(ns1, path='/v1.0/citystatistics')
