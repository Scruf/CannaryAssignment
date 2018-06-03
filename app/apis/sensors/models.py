from app.extensions import db


class Sensor(db.Document):
	device_uuid = db.StringField()
	sensort_type_options = ["temperature", "humidity"]
	sensor_type = db.StringField(choices=sensort_type_options)
	sensor_value = db.FloatField(min_value=0.0, max_value=100.0)
	sensor_reading_time = db.DateTimeField()
