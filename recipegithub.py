import urllib
from recipemarkdown import parse_recipe_markdown

class GitHubBridge(object):

  def __init__(self, github_repo_api_base, requests):
    self._api_base = github_repo_api_base
    self._requests = requests
    self._repo = github_repo_api_base.split('repos/')[1]

  def list(self):
    response = []
    r = self._requests.get(self._api_base + '/contents')
    if r.ok:
      contents = r.json() #json.loads(r.text)
      for item in contents:
        if item['name'].startswith('recipe'):
          response.append(self._handle_recipe(item))
    return response

  def search(self, query):
    response = []
    r = self._requests.get('https://api.github.com/search/code?q=%s+repo:%s' %
        (urllib.quote_plus(query), self._repo))
    if r.ok:
      contents = r.json()
      if contents['total_count'] > 0:
        for item in contents['items']:
          if item['name'].startswith('recipe-'):
            response.append({'name': item['name'], 'score': item['score']})
    return response

  def _handle_recipe(self, item):
    obj = {}
    obj['name'] = item['name']
    url = item['url']
    r = self._requests.get(url, headers={"Accept": "application/vnd.github.3.raw"})
    if r.ok:
      markdown = r.text
      obj = parse_recipe_markdown(markdown, obj, self._raw_base_url())
    return obj

  def _raw_base_url(self):
    return self._api_base.replace(
        'api.github.com', 'github.com').replace('repos/', '') + '/raw/master/'




