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




path = "random{}/{}.json".format(46,1)
response = (authed_session.get(db+path))
#print(dict(response.json()))
my_response = dict(response.json())
print(f"my response in send hit of lives is {my_response}")
prev_lives = my_response['lives']

print(type(prev_lives))