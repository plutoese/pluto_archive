# coding = UTF-8

from flask_restplus import Api

from .demoAPI import api as ns1
from .api_city_statistics import api as ns2

api = Api(
    title='DataSource',
    author = 'Glen',
    version='1.0',
    description='数据源接口',
)

api.add_namespace(ns1, path='/v1.0/demoapi')
api.add_namespace(ns2, path='/v1.0/citystatistics')
