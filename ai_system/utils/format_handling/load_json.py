import json


def json_load(data):
    with open(data, 'r') as f:
        task = json.load(f)
    return task
