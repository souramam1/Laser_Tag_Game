import requests,time,random
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

db = "https://laser-tag-testing-default-rtdb.europe-west1.firebasedatabase.app//"

keyfile = "laser-tag-testing-firebase-adminsdk-6h09n-67f1530174.json"

scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database"
]

# Authenticate a credential with the service account (change to use your private key)
credentials = service_account.Credentials.from_service_account_file(keyfile, scopes=scopes)

# Use the credentials object to authenticate a Requests session.
authed_session = AuthorizedSession(credentials)

# Define the database URL (change to use your database)
db = "https://laser-tag-testing-default-rtdb.europe-west1.firebasedatabase.app/" 
    

import uuid
unique = uuid.uuid4()

i_d = 0
hit = 0
swoosh = 1
join = 0
game_played = 0



#sending in hit
path = "statistics_test/{}.json".format(unique)
data = {"id":i_d,
    "time":time.time(),
    "hit": hit,
    "swoosh" : swoosh,
    "joining": join,
    "game_played": game_played,
    "lives": "X"}   

print("Writing {} to {}".format(data, path))

response = authed_session.put(db+path, json=data)

if response.ok:  #error checking
    print("Created new node named {}".format(response.json()["id"]))
else:
    raise ConnectionError("Could not write to database: {}".format(response.text))

    