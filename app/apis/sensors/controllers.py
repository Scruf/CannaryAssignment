import json
from uuid import uuid4
from datetime import datetime
from .models import Sensor
#Create function will check to see if the device is already present 
#if so than update it otherwise create it
def create(args):
	#Check to make sure that sensor type is either humidity or temperature
	if args.sensor_type not in ['humidity', 'temperature']:
		#If its not than we return error with 400 error code
		return {
			"error":"Sensor type must be humidity or temperature"
		}, 400
	#Check to make sure that sensor value is in the range 
	if args.sensor_value < 0.0 or args.sensor_value > 100.0:
		#Its is not so we send the error back and 400 
		return {
			"error":"Sensor value must be in range(0.0, 100.0)"
		}, 400
	try:
		#Connvert time to datetime object 
		args.sensor_reading_time = datetime.fromtimestamp(args.sensor_reading_time)
		#Update or save sensor information
		sensor = Sensor.objects(device_uuid=args.device_uuid).update_one(
			set__sensor_type = args.sensor_type,
			set__sensor_value = args.sensor_value,
			set__sensor_reading_time = args.sensor_reading_time,
			upsert=True
		)
		#Return susccess message back with 200 code back
		return {
			"data":"Sensor reading was saved successfully"
		}

	except Exception as ex:
		#If there was an error return error message and 500 back
		return {
			"error":"Could not save to the database"
		}, 500

def get_sensor_data(args):
	#Check to see if there any parameters in query string
	if not args:
		#There is no parameters so we return an error message with 400
		return {
			"error":"Empty query parameters cannot be left empty"
		},400
	#Check to see if start time or end time is present
	if not args.get('start_time') or not args.get('end_time'):
		#Its not so we return an error with a 400 status code
		return {
			"error":"Start Time or End time has to be present in the query"
		}, 400
	#Create query to filter entries
	query = {
		"sensor_reading_time":{
		"$gte":datetime.fromtimestamp(int(args.get('start_time')[0])), "$lte":datetime.fromtimestamp(int(args.get('end_time')[0]))
	}}
	try:
		#Call the query
		sensor_query = Sensor.objects(__raw__=query)
		#Since to json on the model will return string representation of object we json.loads to get python objects back
		return [json.loads(sensor.to_json()) for sensor in sensor_query],200
	except Exception as ex:
		#There was an error during fetching we return 500 and error message
		return {"error":"Could not retrive sensor information"},500