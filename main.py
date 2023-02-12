from flask import Flask, request, make_response
import threading
import os
import signal
import requests,time,random,uuid
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from join_db_flask import access_db

# db definitions #
db = "https://laser-tag-testing-default-rtdb.europe-west1.firebasedatabase.app/"
#path = ".json"
keyfile = "laser-tag-testing-firebase-adminsdk-6h09n-67f1530174.json"
scopes = [
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/firebase.database"
]
credentials = service_account.Credentials.from_service_account_file(keyfile, scopes=scopes)
authed_session = AuthorizedSession(credentials)

#variable definitions
game_status = 0 #this will be 0 when a game is not currently being played - and 1 when a game is being played

# functions #
class NewThreadedTask(threading.Thread):
     def __init__(self):
         super(NewThreadedTask, self).__init__()
 
     def run(self):
         n = 0
         print("inside threading subroutine")
         
         while n <= 500:
             print(f"n is {n}")
             time.sleep(1)
             n += 1
    
         print('Threaded task has been completed')



def response_check(response):
    
    if response.ok:  #error checking
        print("Created new node named {}".format(response.json()["id"]))
    else:
        raise ConnectionError("Could not write to database: {}".format(response.text))
    
def send_hit(player_i_d, max_num):
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
    

def table_time_made(response): #time creation definition #change this to check if the game_play entry in 0th row of most recent table is 0
    
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

def table_game_played_check(response): #time creation definition #change this to check if the game_play entry in 0th row of most recent table is 0
    
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
    
    game_played_check = my_response[f'{recent_game}'][0]['game_played'] #time most recent game_play was initialised
    return game_played_check, game_tables, mx

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

def init_new_game_play_check(game_tables,max_num): #if time limit to join game has been exceeded new game is started
    print("in init_new game_play")
    i_d = 0
    hit = 0
    swoosh = 0
    join = 1
    game_played = 0
    #num = int(game_tables[-1][-1]) + 1
    num = max_num + 1
    print(max_num)
    
    #send(num,i_d,hit,swoosh,join,uuid)
    path = "random{}/{}.json".format(num,i_d)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join,
        "game_played": game_played}    #format of the data you are delivering to table

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
    
def join_new_game_play_check(game_tables,max_num):
    print("in join_new game_play")
    i_d = 1
    hit = 0
    swoosh = 0
    join = 1
    game_played = 0

    num = max_num
    print(num)
    
    path = "random{}/{}.json".format(num,i_d)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join,
        "game_played": game_played}    #format of the data you are delivering to table

    print("Writing {} to {}".format(data, path))
    #response = requests.post(db+path, json=data) #function which actually adds the info to the table
    response = authed_session.put(db+path, json=data)
    response_check(response)


def initialise_game_play(time_check,game_tables,max_num):
    
    if time.time() - time_check >= 30:
        #make new table with index number greater than most recent table in database and put in one entry (0th entry)
        init_new_game(game_tables,max_num)
        player_i_d = 0
    else:
        #join this table as a player
        join_new_game(game_tables,max_num)
        player_i_d = 1
    
    return player_i_d

#This function is the new one i added
def initialise_game_play_not_w_time(game_played,game_tables,max_num,game_status):
    print("in initialise game play not w time ")
    
    
    if (game_played == 1) & (game_status == 0): #the most recent game has already been played but no game is currently playing
        #make new table with index number greater tha most recent table in database and put in one entry (0th entry)
        init_new_game_play_check(game_tables,max_num) #this function needs to have value for game_played field so that it can be read
        player_i_d = 0
    elif (game_played == 0) & (game_status == 0):
        #join this table as a player
        join_new_game_play_check(game_tables,max_num)
        player_i_d = 1
    else:
        player_i_d = -1 # when player id is -1 means player cannot join -- flash an LED
    
    return player_i_d

app: Flask = Flask(__name__)

def main():

    app.run(host="0.0.0.0", port=2000) # Blocking

# Primary page to load

@app.route("/")
def main_page():
    return "Wooo!"

@app.route("/join", methods = ['GET'] )
def join_game():
    game_tables = []
    time_check = 0
    max_num = 0
    path = ".json"
    print("in join game")
    access_db()
    
    # query = "?orderBy=\"n\"&equalTo=3&print=pretty"
    response = authed_session.get(db+path)
    print(response)
    
    if response.ok:
        
        #table_timing = table_time_made(response)
        
        #added just now (checks if most recent game has already been played : the game_played flag in 0th entry will be turned to 1 when it has)
        game_played_check = table_game_played_check(response)
        
        # time_check = table_timing[0]
        # game_tables = table_timing[1]
        # max_num = table_timing[2]

        game_played = game_played_check[0]
        print(f"game played is {game_played}")
        game_tables = game_played_check[1]
        print(game_tables)
        max_num = game_played_check[2]
        print(max_num)
        
        
        #player_i_d = initialise_game_play(time_check,game_tables,max_num) #either joining or initialising a new game db
        
        #also added just now
        player_i_d = initialise_game_play_not_w_time(game_played,game_tables,max_num,game_status)
        
        #resp = make_response(f'{ "body" : {player_i_d} }')
        resp = make_response(f"""{{"player_id": {player_i_d}}}""")
        return resp
        
        #send_hit(player_i_d)
    else:
        raise ConnectionError("Could not access database: {}".format(response.text))
    


@app.route("/swoosh", methods = ['GET', 'POST'] ) 
def swooshed():
    i_d = request.json
    print(i_d)
    resp = make_response('{ "body" : "key" }')
    return resp


@app.route("/play_game", methods = ['GET', 'POST'] ) 
def background_task():
    new_thread = NewThreadedTask()
    new_thread.start()
    # optionally wait for task to complete
    new_thread.join()
    print("THREAD MERGED AT END OF THREAD CAST")
    return {'thread': 'completed'}, 200

@app.route("/game_test", methods = ['GET', 'POST'] ) 
def test():
    print("game test is being called during the thread")
    resp = make_response('{ "returning from call" : "hello" }')
    #print("IN THE GAME TEST FUNCTION - IT WAS CALLED")
    return resp
    


    
    
    
if __name__ == '__main__':
    main()