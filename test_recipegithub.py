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
SEARCH = """
{
  "total_count": 1,
  "items": [
    {
      "name": "recipe-super-simple-guacamole.md",
      "path": "recipe-super-simple-guacamole.md",
      "sha": "c0716101598f4f434da91ec96f1d2219879aeb5b",
      "url": "https://api.github.com/repositories/16055826/contents/recipe-super-simple-guacamole.md?ref=ef55297fc9d743b17d9aae467551bb1337cc9fca",
      "git_url": "https://api.github.com/repositories/16055826/git/blobs/c0716101598f4f434da91ec96f1d2219879aeb5b",
      "html_url": "https://github.com/dps/recipes/blob/ef55297fc9d743b17d9aae467551bb1337cc9fca/recipe-super-simple-guacamole.md",
      "repository": {
        "id": 16055826,
        "name": "recipes",
        "full_name": "dps/recipes",
        "owner": {
          "login": "dps",
          "id": 237355,
          "gravatar_id": "ca0bcee0ee45afe52973d86721b72a93",
          "url": "https://api.github.com/users/dps"
        },
        "private": false,
        "html_url": "https://github.com/dps/recipes",
        "description": "recipes",
        "fork": false,
        "url": "https://api.github.com/repos/dps/recipes"
      },
      "score": 2.1095433
    }
  ]
}
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
  assert 'https://api.github.com/repos/test/test/contents' == fr._requested[0][0]
  assert 'https://api.github.com/repos/dps/recipes/contents/recipe-beef-brisket-chili.md?ref=master' == fr._requested[1][0]
  assert len(result) == 1
  assert result[0]['title'] == 'Silly Test recipe'

def test_search():
  fr = FakeRequests()
  fr.set_next_reponse(FakeResponse(True, SEARCH))
  ghb = GitHubBridge('https://api.github.com/repos/test/test', fr)
  result = ghb.search('test!')
  assert fr._requested[0][0].find('q=test%21') >= 0 #%21 is ! url encoded
  assert result[0]['score'] == 2.1095433
  assert result[0]['name'] == 'recipe-super-simple-guacamole.md'
