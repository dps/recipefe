import random
import string
import time

ONE_DAY = 24 * 60 * 60
ONE_WEEK = 7 * ONE_DAY

class KeyValStore(object):

  def __init__(self, redis, instance, github_bridge):
    self._redis = redis
    self._instance = instance
    self._ghb = github_bridge

  def _key_recipe(self, recipe, key):
  	return self._instance + ':recipe:' + str(recipe) + ':' + key

  def list(self):
    if not self._redis.exists(self._instance + ':list'):
      for recipe in self._ghb.list():
        name = recipe['name']
        self._redis.sadd(self._instance + ':list', name)
        self._redis.set(self._key_recipe(name, 'title'), recipe['title'])
        self._redis.set(self._key_recipe(name, 'summary'), recipe['summary'])
        self._redis.set(self._key_recipe(name, 'ingredients'), recipe['ingredients'])
        self._redis.set(self._key_recipe(name, 'steps'), recipe['steps'])
      self._redis.expire(self._instance + ':list', ONE_DAY)

    return self._redis.smembers(self._instance + ':list')


