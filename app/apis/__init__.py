from flask_restplus import Api
from .sensors import api as sensors

api = Api(
	title = 'canary assignment',
	description = 'Sensors api using mongoengine and flask_restplus'
)
#set sensors endpoint
api.add_namespace(sensors, path='/sensors')