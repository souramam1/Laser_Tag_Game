import requests,time,uuid
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession

#db definitions
db = "https://laser-tag-testing-default-rtdb.europe-west1.firebasedatabase.app/"
#path = "timeseries.json"
path = ".json"
keyfile = "laser-tag-testing-firebase-adminsdk-6h09n-67f1530174.json"
scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database"
]
# Authenticate a credential with the service account (change to use your private key)
credentials = service_account.Credentials.from_service_account_file(keyfile, scopes=scopes)
# Use the credentials object to authenticate a Requests session.
authed_session = AuthorizedSession(credentials)


def response_check(response):
    
    if response.ok:  #error checking
        print("Created new node named {}".format(response.json()["id"]))
    else:
        raise ConnectionError("Could not write to database: {}".format(response.text))
    
def send_hit(player_i_d):
    import uuid
    
    unique = uuid.uuid4()
    
    i_d = player_i_d
    hit = 1
    swoosh = 0
    join = 0
    
    num = max_num 
    print(max_num)
    
    #send(num,i_d,hit,swoosh,join,uuid)
    path = "random{}/{}.json".format(num,unique)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join}    #format of the data you are delivering to table

    print("Writing {} to {}".format(data, path))
    #response = requests.post(db+path, json=data) #function which actually adds the info to the table
    response = authed_session.put(db+path, json=data)
    #response_check(response)
    

def max_table_num(game_tables):
    table_nums = []
    for word in game_tables:
        int_num = int(word.split("random")[1])
        table_nums.append(int_num)
        recent_num = max(table_nums)
        
    return recent_num
    

def table_time_made(): #time creation definition
    
    my_response = dict(response.json())
    tables = my_response.keys()
    game_tables = []
    
    for item in tables:
        if item.find("random") != -1: #this will be changed to "gameplay" for the actual simulation
            game_tables.append(item)
            print("table found : checking time creation!")
        
    #recent_game = game_tables[-1]
    mx = max_table_num(game_tables)
    recent_game = "random"+f"{mx}" #change random for game_tables
    print(recent_game)
    
    t_created = my_response[f'{recent_game}'][0]['time'] #time most recent game_play was initialised
    return t_created, game_tables, mx

def init_new_game(game_tables,max_num): #if time limit to join game has been exceeded new game is started
    
    i_d = 0
    hit = 0
    swoosh = 0
    join = 1
    #num = int(game_tables[-1][-1]) + 1
    num = max_num + 1
    print(max_num)
    
    #send(num,i_d,hit,swoosh,join,uuid)
    path = "random{}/{}.json".format(num,i_d)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join}    #format of the data you are delivering to table

    print("Writing {} to {}".format(data, path))
    #response = requests.post(db+path, json=data) #function which actually adds the info to the table
    response = authed_session.put(db+path, json=data)
    response_check(response)
    

def join_new_game(game_tables,max_num):
    
    i_d = 1
    hit = 0
    swoosh = 0
    join = 1

    num = max_num
    print(num)
    
    path = "random{}/{}.json".format(num,i_d)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join}    #format of the data you are delivering to table

    print("Writing {} to {}".format(data, path))
    #response = requests.post(db+path, json=data) #function which actually adds the info to the table
    response = authed_session.put(db+path, json=data)
    response_check(response)


def initialise_game_play():
    if time.time() - time_check >= 10000:
        #make new table with index number greater than most recent table in database and put in one entry (0th entry)
        init_new_game(game_tables,max_num)
        player_i_d = 0
    else:
        #join this table as a player
        join_new_game(game_tables,max_num)
        player_i_d = 1
    
    return player_i_d
    
#query = "?orderBy=\"$key\"&startAt=\"{}\"&endAt=\"{}\"".format(int(time.time()-3600), int(time.time()))
query = "?orderBy=\"n\"&equalTo=3&print=pretty"
#response = authed_session.get(db+path+query)
response = authed_session.get(db+path)

if response.ok:
    
    table_timing = table_time_made()
    time_check = table_timing[0]
    game_tables = table_timing[1]
    max_num = table_timing[2]
    
    
    player_i_d = initialise_game_play() #either joining or initialising a new game db
    
    send_hit(player_i_d)
    
    
    
    
    
    
    
    
else:
    raise ConnectionError("Could not access database: {}".format(response.text))