from flask_restplus import Namespace, Resource, reqparse
from flask import jsonify, request
from . import controllers
api = Namespace('sensors')
#create_sensor parser will enforce required data and parse the data which will be passed to the controller
#For further operations
def create_sensor():
	parser = reqparse.RequestParser()
	parser.add_argument("device_uuid", type=str, required=True)
	parser.add_argument("sensor_type", type=str, required=True)
	parser.add_argument("sensor_value", type=float, required=True)
	parser.add_argument("sensor_reading_time", type=int, required=True)
	return parser

#Basic sensor crud operations
@api.route('/')
class Sensors(Resource):
	#tell the put to expect the arguments 
	@api.expect(create_sensor())
	def put(self):
		#get the arguments from the payload
		parser = create_sensor()
		#Save them into args and pass it to controller
		args = parser.parse_args()
		return controllers.create(args)

	
	def get(self):
		return controllers.get_sensor_data(dict(request.args))
