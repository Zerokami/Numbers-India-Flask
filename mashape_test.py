import requests
import json

r =requests.get("https://dndcheck.p.mashape.com/index.php?mobilenos={}".format('8790113921'), headers ={
    "X-Mashape-Key": "obqeZksomumshUE8EvVYIqvRXWNsp1waVYpjsnUOa3brsHCokK"
  })

JSON = json.loads(r.text)

print JSON

print len(JSON)

j = JSON[0]

print j