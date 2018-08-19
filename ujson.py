# Wrapper to json so we can test ujson dependent code
import json

def loads(string):
    return json.loads(string)