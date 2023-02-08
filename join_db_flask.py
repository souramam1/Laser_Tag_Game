import requests,time,random,uuid
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

def access_db():
    
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

    i_d = 1
    hit = 0
    swoosh = 0
    join = 1

    uuid = uuid.uuid4()


    game_tables = ['random', 'random1', 'random2', 'random3', 'random4']

    num = int(game_tables[-1][-1])
    print(num)
        
    path = "random{}/{}.json".format(num,uuid)
    data = {"id":i_d,
            "time":time.time(),
            "hit": hit,
            "swoosh" : swoosh,
            "joining": join}    #format of the data you are delivering to table

    print("Writing {} to {}".format(data, path))
    #response = requests.post(db+path, json=data) #function which actually adds the info to the table
    response = authed_session.put(db+path, json=data)

    if response.ok:  #error checking
        print("Created new node named {}".format(response.json()["id"]))
    else:
        raise ConnectionError("Could not write to database: {}".format(response.text))