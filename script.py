import urllib
import urllib.request
contents = urllib.request.urlopen("http://127.0.0.1:8000/api/logic/action_sample/").read()

import urllib.request
with urllib.request.urlopen('http://python.org/') as response:
    html = response.read()

