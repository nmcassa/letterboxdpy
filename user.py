import json
from json import JSONEncoder

class User:
    def __init__(self, username, stats):
        self.username = username
        self.stats = stats

    def jsonify(self):
        return json.dumps(self, indent=4,cls=Encoder)

class Encoder(JSONEncoder):
    def default(self, o):
        return o.__dict__
