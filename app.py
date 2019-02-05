import json
import os
import redis
import requests
from flask import Flask, Response, send_file, request, render_template
from keyvalstore import KeyValStore
from recipegithub import GitHubBridge

app = Flask(__name__)
app.debug = True #hup

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
  limit = request.args.get('limit')
  if limit != None:
    limit = int(limit)
  page = request.args.get('page')
  if page != None:
    page = int(page)
  response = keyval.list(page=page, limit=limit)
  return je.encode(response)

@app.route('/api/search')
def searchapi():
  limit = request.args.get('limit')
  page = request.args.get('page')
  if limit != None:
    limit = int(limit)
  page = request.args.get('page')
  if page != None:
    page = int(page)
  q = request.args.get('q')
  return je.encode(keyval.search(q, page=page, limit=limit))

@app.route('/')
def index():
  recipes = keyval.list()['recipes']
  return render_template('index.html', recipes=recipes)

@app.route('/recipes/<name>')
def recipe(name):
  recipe = keyval.recipe(name)
  return render_template('recipe.html', recipe=recipe)

@app.route('/search')
def search():
  q = request.args.get('q')
  results = keyval.search(q)['recipes']
  return render_template('search.html', results=results, q=q)
