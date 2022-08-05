import urllib
import urllib.request
import urllib.parse

contents = urllib.request.urlopen("http://127.0.0.1:8000/api/logic/action_sample/").read()

with urllib.request.urlopen('http://python.org/') as response:
    html = response.read()

print(html)


# -- Get video data and transcriptions as output to Kafka stream as json object
# -- consume video data to summarization app, produce summarization.
# -- Get tweets as output to Kafka stream as json
# -- send data to hasura endpoint, into psql in hasura node
# -- associate tweets and twitter data with users
# -- login logic, realtime users ID
# -- pass user id to recommender consumer
# -- recommender produces video summarization.

url = 'http://127.0.0.1:8000/api/logic/action_sample/'
values = {'twitter_id':'948374', 'location':'', 'bio':'', 'tweet':'Will elon buy twitter?'}; print(values)
data = urllib.parse.urlencode(values)
data = data.encode('ascii') # data should be bytes
req = urllib.request.Request(url)
with urllib.request.urlopen(req) as response:
   the_page = response.read()