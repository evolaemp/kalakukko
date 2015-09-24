from django.core.serializers.json import DjangoJSONEncoder

import json


def make_json(python_things):
	"""
	Converts Python things to JSON things.
	"""
	return json.dumps(python_things, cls=DjangoJSONEncoder)


def read_json(json_things):
	"""
	Converts JSON things to Python things.
	"""
	if isinstance(json_things, bytes):
		json_things = json_things.decode()
	return json.loads(json_things)

