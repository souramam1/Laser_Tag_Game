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



def calcAcc(current_game_num):

    #path = f"random{current_game_num}.json"
    path = "statistics_test.json"

    response = (authed_session.get(db+path))

    my_response = dict(response.json())


    if response.ok:
        countHashTable = {}

        for entry in my_response.values():
            id = entry["id"]
            if id in countHashTable:
                countHashTable[id][0] += 1
                countHashTable[id][1] += entry["hit"]
            else:
                countHashTable[id] = [1, entry["hit"]]

        accuracies = {}
        for id, counts in countHashTable.items():
            accuracies[id] = counts[1]/counts[0]
            
            
            player_0_acc = accuracies[0]
            player_1_acc = accuracies[1]
            
            
            


        
        print(accuracies)
        response = make_response()
        return accuracies

    else:
        raise ConnectionError("Could not access database: {}".format(response.text))


calcAcc(38)