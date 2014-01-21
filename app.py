import json
import os
import redis
import requests
from flask import Flask, Response, send_file
from keyvalstore import KeyValStore

app = Flask(__name__)
app.debug = False

je = json.JSONEncoder()

pubkeyval = KeyValStore(redis.StrictRedis(
    host='spadefish.redistogo.com', 
    port=9148, 
    db=0,
    password=os.environ('REDISKEY')),
    'recipefe')

GIT_REPO = 'https://api.github.com/repos/dps/recipes'

@app.route('/api/recipe/<name>')
def recipe(name):
  return ''

@app.route('/api/list')
def list():
  response = []
  r = requests.get(GIT_REPO + '/contents')
  if r.ok:
    contents = json.loads(r.text)
    for item in contents:
      if item['name'].startswith('recipe'):
        response.append(item['name'])
  return je.encode(response)


