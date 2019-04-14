import json
import random
import string
import time

ONE_DAY = 24 * 60 * 60
ONE_WEEK = 7 * ONE_DAY

je = json.JSONEncoder()
jd = json.JSONDecoder()

def e(obj):
  return je.encode(obj)

def d(jso):
  if jso:
    return jd.decode(jso)
  else:
    return ''

class KeyValStore(object):

  def __init__(self, redis, instance, github_bridge):
    self._redis = redis
    self._instance = instance
    self._ghb = github_bridge
    self._memoized_list = None

  def _key_recipe(self, recipe, key):
  	return self._instance + ':recipe:' + str(recipe) + ':' + key

  def list(self, verbose=False, limit=None, page=None):
    if self._memoized_list != None:
      return self._memoized_list
    if not self._redis.exists(self._instance + ':list'):
      for recipe in self._ghb.list():
        name = recipe['name']
        self._redis.sadd(self._instance + ':list', name)
        self._redis.set(self._key_recipe(name, 'title'), recipe['title'])
        self._redis.set(self._key_recipe(name, 'ingredients'), e(recipe['ingredients']))
        self._redis.set(self._key_recipe(name, 'steps'), e(recipe['steps']))
        if recipe.has_key('serving'):
          self._redis.set(self._key_recipe(name, 'serving'), e(recipe['serving']))
        if recipe.has_key('summary'):
          summary = '\n'.join(recipe['summary'])
          self._redis.set(self._key_recipe(name, 'summary'), summary)
        if recipe.has_key('img'):
          self._redis.set(self._key_recipe(name, 'img'), recipe['img'])
      self._redis.expire(self._instance + ':list', ONE_DAY)
    response = {}
    recipes = []
    result = list(self._redis.smembers(self._instance + ':list'))
    response['total'] = len(result)
    if limit != None:
      result = result[(page-1)*limit:(page*limit)]
    for name in result:
      recipe = {}
      recipe['name'] = name
      recipe['title'] = self._redis.get(self._key_recipe(name, 'title'))
      recipe['summary'] = self._redis.get(self._key_recipe(name, 'summary'))
      if self._redis.exists(self._key_recipe(name, 'img')):
        recipe['img'] = self._redis.get(self._key_recipe(name, 'img'))
      if verbose:
        recipe['ingredients'] = d(self._redis.get(self._key_recipe(name, 'ingredients')))
        recipe['steps'] = d(self._redis.get(self._key_recipe(name, 'steps')))
        recipe['serving'] = d(self._redis.get(self._key_recipe(name, 'serving')))
      recipes.append(recipe)
    response['recipes'] = recipes
    self._memoized_list = response
    return response

  def recipe(self, name):
    if not self._redis.get(self._key_recipe(name, 'title')):
      return {'error': 'recipe not found'}
    recipe = {}
    recipe['name'] = name
    recipe['title'] = self._redis.get(self._key_recipe(name, 'title'))
    recipe['summary'] = self._redis.get(self._key_recipe(name, 'summary'))
    recipe['ingredients'] = d(self._redis.get(self._key_recipe(name, 'ingredients')))
    recipe['steps'] = d(self._redis.get(self._key_recipe(name, 'steps')))
    recipe['serving'] = d(self._redis.get(self._key_recipe(name, 'serving')))
    recipe['img'] = self._redis.get(self._key_recipe(name, 'img'))
    return recipe

  def search(self, q, limit=None, page=None):
    response = {}
    recipes = []
    results = self._ghb.search(q)
    response['total'] = len(results)
    if limit != None:
      results = results[(page-1)*limit:(page*limit)]
    response['q'] = q
    for result in results:
      name = result['name']
      recipe = {}
      recipe['name'] = name
      recipe['score'] = result['score']
      recipe['title'] = self._redis.get(self._key_recipe(name, 'title'))
      recipe['summary'] = self._redis.get(self._key_recipe(name, 'summary'))
      #recipe['ingredients'] = d(self._redis.get(self._key_recipe(name, 'ingredients')))
      #recipe['steps'] = d(self._redis.get(self._key_recipe(name, 'steps')))
      #recipe['serving'] = d(self._redis.get(self._key_recipe(name, 'serving')))
      recipe['img'] = self._redis.get(self._key_recipe(name, 'img'))
      recipes.append(recipe)
    response['recipes'] = recipes
    return response

