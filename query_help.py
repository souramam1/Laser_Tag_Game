import requests, time
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

db = "https://laser-tag-testing-default-rtdb.europe-west1.firebasedatabase.app/"
path = "postlist.json"

keyfile = "laser-tag-testing-firebase-adminsdk-6h09n-67f1530174.json"

scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database"
]

# Authenticate a credential with the service account (change to use your private key)
credentials = service_account.Credentials.from_service_account_file(keyfile, scopes=scopes)
# Use the credentials object to authenticate a Requests session.
authed_session = AuthorizedSession(credentials)

#query = "?orderBy=\"$key\"&startAt=\"{}\"&endAt=\"{}\"".format(int(time.time()-3600), int(time.time()))
query = "?orderBy=\"rnd\"&startAt=0.5&endAt=1.0" 

response = authed_session.get(db+path+query)

if response.ok:
    print(response.json())   
else:
    raise ConnectionError("Could not access database: {}".format(response.text))