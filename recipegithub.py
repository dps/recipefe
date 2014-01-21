import json
from recipemarkdown import parse_recipe_markdown

class GitHubBridge(object):

  def __init__(self, github_repo_api_base, requests):
    self._api_base = github_repo_api_base
    self._requests = requests

  def list(self):
    response = []
    r = self._requests.get(self._api_base + '/contents')
    if r.ok:
      contents = r.json() #json.loads(r.text)
      for item in contents:
        if item['name'].startswith('recipe'):
          response.append(self._handle_recipe(item))
    return response

  def _handle_recipe(self, item):
    obj = {}
    obj['name'] = item['name']
    url = obj['url']
    r = self._requests.get(url, headers={"Accept": "application/vnd.github.3.raw"})
    if r.ok:
      markdown = r.text
      obj = parse_recipe_markdown(markdown, obj, url)




