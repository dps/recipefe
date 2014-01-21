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
  return jd.decode(jso)

class KeyValStore(object):

  def __init__(self, redis, instance, github_bridge):
    self._redis = redis
    self._instance = instance
    self._ghb = github_bridge

  def _key_recipe(self, recipe, key):
  	return self._instance + ':recipe:' + str(recipe) + ':' + key

  def list(self, verbose=False):
    if not self._redis.exists(self._instance + ':list'):
      for recipe in self._ghb.list():
        name = recipe['name']
        self._redis.sadd(self._instance + ':list', name)
        self._redis.set(self._key_recipe(name, 'title'), recipe['title'])
        self._redis.set(self._key_recipe(name, 'summary'), e(recipe['summary']))
        self._redis.set(self._key_recipe(name, 'ingredients'), e(recipe['ingredients']))
        self._redis.set(self._key_recipe(name, 'steps'), e(recipe['steps']))
        self._redis.set(self._key_recipe(name, 'img'), recipe['img'])
      self._redis.expire(self._instance + ':list', ONE_DAY)
    response = []
    for name in self._redis.smembers(self._instance + ':list'):
      recipe = {}
      recipe['name'] = name
      recipe['title'] = self._redis.get(self._key_recipe(name, 'title'))
      recipe['summary'] = d(self._redis.get(self._key_recipe(name, 'summary')))
      recipe['img'] = self._redis.get(self._key_recipe(name, 'img'))
      if verbose:
        recipe['ingredients'] = d(self._redis.get(self._key_recipe(name, 'ingredients')))
        recipe['steps'] = d(self._redis.get(self._key_recipe(name, 'steps')))
      response.append(recipe)
    return response

  def recipe(self, name):
    if not self._redis.get(self._key_recipe(name, 'title')):
      return {'error': 'recipe not found'}
    recipe = {}
    recipe['name'] = name
    recipe['title'] = self._redis.get(self._key_recipe(name, 'title'))
    recipe['summary'] = d(self._redis.get(self._key_recipe(name, 'summary')))
    recipe['ingredients'] = d(self._redis.get(self._key_recipe(name, 'ingredients')))
    recipe['steps'] = d(self._redis.get(self._key_recipe(name, 'steps')))
    recipe['img'] = self._redis.get(self._key_recipe(name, 'img'))
    return recipe


