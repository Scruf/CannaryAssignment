import random
from uuid import uuid4
from datetime import datetime
from faker import Faker
from .models import Sensor

def create_sample():
	sample_list = []
	fake = Faker()
	for _ in range(1, 100):
		sample_dict = {
			"device_uuid":uuid4().hex,
			"sensor_type":"temperature",
			"sensor_value":random.uniform(0.0, 100.0),
			"start_time":fake.date_this_year(before_today=False, after_today=True),
			"end_time":fake.date_this_year(before_today=False, after_today=True),
			"sensor_reading_time":fake.date_this_year(before_today=False, after_today=True)
		}
		sensor = Sensor(**sample_dict)
		sensor.save()

def create(args):
	if args.sensor_type not in ['humidity', 'temperature']:
		return {
			"error":"Sensor type must be humidity or temperature"
		}, 400
	if args.sensor_value < 0.0 or args.sensor_value > 100.0:
		return {
			"error":"Sensor value must be in range(0.0, 100.0)"
		}, 400
	try:
		args.sensor_reading_time = datetime.fromtimestamp(args.sensor_reading_time)
		sensor = Sensor.objects(device_uuid=args.device_uuid).update_one(
			set__sensor_type = args.sensor_type,
			set__sensor_value = args.sensor_value,
			set__sensor_reading_time = args.sensor_reading_time,
			upsert=True
		)
		return {
			"data":"Sensor reading was saved successfully"
		}
	except Exception as ex:
		return {
			"error":"Could not save to the database"
		}, 500
def get_sensor_data(args):
	if not args:
		return {
			"error":"Empty query parameters cannot be left empty"
		},400
	if not args.get('start_time') or not args.get('end_time'):
		return {
			"error":"Start Time or End time has to be present in the query"
		}, 400
	query = {
		"sensor_reading_time":{
		"$gte":datetime.fromtimestamp(int(args.get('start_time')[0])), "$lte":datetime.fromtimestamp(int(args.get('end_time')[0]))
	}}
	print(Sensor.objects(__raw__=query))