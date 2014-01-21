import json
import os
import redis
import requests
from flask import Flask, Response, send_file
from keyvalstore import KeyValStore
from recipegithub import GitHubBridge

app = Flask(__name__)
app.debug = True

GIT_REPO = 'https://api.github.com/repos/dps/recipes'

je = json.JSONEncoder()
github = GitHubBridge(GIT_REPO, requests)

keyval = KeyValStore(redis.StrictRedis(
    host='spadefish.redistogo.com', 
    port=9148, 
    db=0,
    password=os.environ['REDISKEY']),
    'recipefe',
    github)

@app.route('/api/recipe/<name>')
def recipe(name):
  return je.encode(keyval.recipe(name))

@app.route('/api/list')
def list():
  response = keyval.list()
  return je.encode(response)


