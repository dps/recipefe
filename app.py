import json
import os
import redis
import requests
from flask import Flask, Response, send_file, request, render_template
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
def recipeapi(name):
  return je.encode(keyval.recipe(name))

@app.route('/api/list')
def listapi():
  response = keyval.list()
  return je.encode(response)

@app.route('/api/search')
def searchapi():
  q = request.args.get('q')
  return je.encode(keyval.search(q))

@app.route('/')
def index():
  recipes = keyval.list()
  return render_template('index.html', recipes=recipes)

@app.route('/recipe/<name>')
def recipe(name):
  recipe = keyval.recipe(name)
  return render_template('recipe.html', recipe=recipe)

@app.route('/search')
def search():
  q = request.args.get('q')
  results = keyval.search(q)
  return render_template('search.html', results=results, q=q)
