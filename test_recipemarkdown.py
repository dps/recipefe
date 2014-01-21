from recipemarkdown import parse_recipe_markdown

def test_parse():
  doc = """
Super simple guacamole
======================
![Super simple guacamole](imgs-super-simple-guacamole/main.jpg "Super simple guacamole")


Some guacamole recipes call for many ingredients and can be a pain to prepare.  This super simple guac can be thrown together in a couple of minutes and tastes great.

Ingredients
-----------
- 2 ripe avocados
- 1 lime
- 2 tbsp cilantro

Steps
-----
1. Use a spoon to scoop the flesh of the avocados into a bowl.
2. Mash with a fork until fairly smooth and creamy.  Preserve some small solid chunks to add texture.
3. Add the juice of the lime.
![juicing the lime](imgs-super-simple-guacamole/step-3-lime.jpg "Juicing the lime")
4. Add the cilantro.
5. Mix thoroughly.

Serving
-------
Great with tortilla chips, in tacos and burritos.
"""
  parsed = parse_recipe_markdown(doc, {'name': 'super-simple-guacamole'}, 'http://www/')
  assert parsed != None
  assert parsed['name'] == 'super-simple-guacamole'
  assert parsed['title'] == 'Super simple guacamole'
  assert len(parsed['serving']) == 1
  assert len(parsed['ingredients']) == 3
  assert len(parsed['steps']) == 5
  assert len(parsed['summary']) == 1
  assert parsed['img'] == 'http://www/imgs-super-simple-guacamole/main.jpg'
  assert parsed['steps'][2]['img'] == 'http://www/imgs-super-simple-guacamole/step-3-lime.jpg'
  assert not parsed.has_key('error')

def test_missing_sections():
  doc = ""
  # Ensure no exception thrown here
  parsed = parse_recipe_markdown(doc, {'name': 'test'}, 'http://www/')
  assert parsed['name'] == 'test'
  doc = """
Super simple guacamole
======================
"""
  parsed = parse_recipe_markdown(doc, {'name': 'test'}, 'http://www/')
  assert parsed['title'] == 'Super simple guacamole'
  assert parsed.has_key('error') # 'Some required sections missing: ingredients, steps'
