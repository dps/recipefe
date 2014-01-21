import json
from recipegithub import GitHubBridge

CONTENTS = """
[
  {
    "name": "LICENSE",
    "path": "LICENSE",
    "sha": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    "size": 0,
    "url": "https://api.github.com/repos/dps/recipes/contents/LICENSE?ref=master",
    "html_url": "https://github.com/dps/recipes/blob/master/LICENSE",
    "git_url": "https://api.github.com/repos/dps/recipes/git/blobs/e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    "type": "file",
    "_links": {
      "self": "https://api.github.com/repos/dps/recipes/contents/LICENSE?ref=master",
      "git": "https://api.github.com/repos/dps/recipes/git/blobs/e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
      "html": "https://github.com/dps/recipes/blob/master/LICENSE"
    }
  },
  {
    "name": "README.md",
    "path": "README.md",
    "sha": "3f8785114077f751602493ec1c0b743380bcce02",
    "size": 25,
    "url": "https://api.github.com/repos/dps/recipes/contents/README.md?ref=master",
    "html_url": "https://github.com/dps/recipes/blob/master/README.md",
    "git_url": "https://api.github.com/repos/dps/recipes/git/blobs/3f8785114077f751602493ec1c0b743380bcce02",
    "type": "file",
    "_links": {
      "self": "https://api.github.com/repos/dps/recipes/contents/README.md?ref=master",
      "git": "https://api.github.com/repos/dps/recipes/git/blobs/3f8785114077f751602493ec1c0b743380bcce02",
      "html": "https://github.com/dps/recipes/blob/master/README.md"
    }
  },
  {
    "name": "imgs-beef-brisket-chili",
    "path": "imgs-beef-brisket-chili",
    "sha": "3b182d2c5592b28ded7191cc351bacad5ddfc716",
    "size": null,
    "url": "https://api.github.com/repos/dps/recipes/contents/imgs-beef-brisket-chili?ref=master",
    "html_url": "https://github.com/dps/recipes/tree/master/imgs-beef-brisket-chili",
    "git_url": "https://api.github.com/repos/dps/recipes/git/trees/3b182d2c5592b28ded7191cc351bacad5ddfc716",
    "type": "dir",
    "_links": {
      "self": "https://api.github.com/repos/dps/recipes/contents/imgs-beef-brisket-chili?ref=master",
      "git": "https://api.github.com/repos/dps/recipes/git/trees/3b182d2c5592b28ded7191cc351bacad5ddfc716",
      "html": "https://github.com/dps/recipes/tree/master/imgs-beef-brisket-chili"
    }
  },
  {
    "name": "recipe-beef-brisket-chili.md",
    "path": "recipe-beef-brisket-chili.md",
    "sha": "3ce61f2b12a92dc802bb067302011d7df40df933",
    "size": 2188,
    "url": "https://api.github.com/repos/dps/recipes/contents/recipe-beef-brisket-chili.md?ref=master",
    "html_url": "https://github.com/dps/recipes/blob/master/recipe-beef-brisket-chili.md",
    "git_url": "https://api.github.com/repos/dps/recipes/git/blobs/3ce61f2b12a92dc802bb067302011d7df40df933",
    "type": "file",
    "_links": {
      "self": "https://api.github.com/repos/dps/recipes/contents/recipe-beef-brisket-chili.md?ref=master",
      "git": "https://api.github.com/repos/dps/recipes/git/blobs/3ce61f2b12a92dc802bb067302011d7df40df933",
      "html": "https://github.com/dps/recipes/blob/master/recipe-beef-brisket-chili.md"
    }
  }
]
"""
MARKDOWN = """
Silly Test recipe
=================
Ingredients
-----------
- 1 sense of humor
Steps
-----
1. Knock Knock
"""

class FakeResponse(object):

  def __init__(self, ok, json):
    self.ok = ok
    self._json = json
    self.text = json

  def json(self):
    return json.loads(self._json)

class FakeRequests(object):

  def __init__(self):
    self._requested = []
    self._next_response = []

  def get(self, url, headers=None):
    self._requested.append((url, headers))
    return self._next_response.pop()

  def set_next_reponse(self, resp):
    self._next_response.append(resp)


def test_list():
  fr = FakeRequests()
  fr.set_next_reponse(FakeResponse(True, MARKDOWN))
  fr.set_next_reponse(FakeResponse(True, CONTENTS))
  ghb = GitHubBridge('https://api.github.com/repos/test/test', fr)
  result = ghb.list()
  assert len(result) == 1
  assert result[0]['title'] == 'Silly Test recipe'

def test_recipe():
  pass

def test_search():
  pass