from flask_restplus import Namespace, Resource, reqparse
from flask import jsonify, request
from . import controllers
api = Namespace('sensors')

def create_sensor():
	parser = reqparse.RequestParser()
	parser.add_argument("device_uuid", type=str, required=True)
	parser.add_argument("sensor_type", type=str, required=True)
	parser.add_argument("sensor_value", type=float, required=True)
	parser.add_argument("sensor_reading_time", type=int, required=True)
	return parser

def query_sensor():
	parser = reqparse.RequestParser()
	parser.add_argument('start_time', type=str, required=True, location='args')
	parser.add_argument('end_time', type=str, required=True, location='args')

@api.route('/')
class Sensors(Resource):

	@api.expect(create_sensor())
	def put(self):
		
		parser = create_sensor()
		args = parser.parse_args()
		return controllers.create(args)

	@api.expect(query_sensor())
	def get(self):
		return controllers.get_sensor_data(dict(request.args))
