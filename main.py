from flask import Flask, request, make_response
import threading
import os
import signal
import json
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

winner = None #"r" or "y"

#variable definitions
#this will be 0 when a game is not currently being played - and 1 when a game is being played

var_list = []  # game_status, game_table_number, value_of create game, winner check
winner_list =[]
player_list = []
game_status = 0 #initialise to zero and set to 1 when game initialised
current_game_num = 'x'
create_game = 1 #intiallise to 0 and set to 1 when kia presses click
winner_check = 0
var_list.append(game_status)
var_list.append(current_game_num)
var_list.append(create_game)
var_list.append(winner_check)

player_dict = {}
colour_dict = {22:'y', 33:'r'}

print(var_list)
# functions 

class NewThreadedTask(threading.Thread):
    #this is where the game play will be defined 
     def __init__(self):
         super(NewThreadedTask, self).__init__()
         
         
     def run(self):
        s_time = time.time()
        print("inside threaded game subroutine")
        
        print("WE ARE IN GAME PLAY")
        winner_check = var_list[3]
        print(F"WINNER CHECK IS {winner_check}")
        while ((time.time()-s_time) <= 40) and (winner_check == 0):
            
            winner_check = var_list[3]
            if (time.time()%10 == 0):
                print(f"winner check is {winner_check}")
            

            game_status = 1
            var_list[0] = game_status
            create_game = 0
            var_list[2] = create_game
            current_game_num = var_list[1]
   
        print('End of threaded game while loop')
        current_game_num = var_list[1]
        game_played_update(current_game_num)
        game_status = 0
        var_list[0] = game_status
        print("End of end of game changes")
        player_list = []
        player_dict = {}
        winner_list = []
        return
             
        
def response_check(response):
    
    if response.ok:  #error checking
        print("Created new node named {}".format(response.json()["id"]))
    else:
        raise ConnectionError("Could not write to database: {}".format(response.text))

def checking_winner(current_game_num):
    print("inside checking winner!!!!!!")
    #query database for win
    print(player_list)
    for players in player_list:
        print(f"inside for loop in checking winner, player is {players}")
        
        path = "random{}/{}.json".format(current_game_num,players)
        response = (authed_session.get(db+path))
        #print(dict(response.json()))
        my_response = dict(response.json())
        prev_lives = my_response['lives']
        winner_list.append(prev_lives)
        losers = winner_list.count(0)
     
    print(winner_list)  
    if len(player_list) - losers == 1:
        print("returning winner check is 1 from checking winner function")
        return 1
    else:
        print("returning winner check is 0 from checking winner function") 
        return 0  
        

def game_played_update(current_game_num):
    
    i_d = 0
    hit = 0
    swoosh = 0
    join = 0
    game_played = 1

    print("int game update after game end")
    
    path = "random{}/0.json".format(current_game_num)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join,
        "game_played": game_played}    #format of the data you are delivering to table
    
    response = authed_session.put(db+path, json=data)  #put creates new nodes
    
    if response.ok:
        print("Ok")
    else:
        raise ConnectionError("Could not write to database: {}".format(response.text))
    time.sleep(1)

    print("Writing {} to {}".format(data, path))
    
def send_hit(game_id, current_game_num):
    print("top of send hit")
    
    import uuid
    unique = uuid.uuid4()
    
    path = "random{}/{}.json".format(current_game_num,game_id)
    response = (authed_session.get(db+path))
    #print(dict(response.json()))
    my_response = dict(response.json())
    print(f"my response in send hit of lives is {my_response}")
    prev_lives = my_response['lives']
    print("after prev lives key error")
    
    i_d = game_id
    hit = 1
    swoosh = 0
    join = 0
    game_played = 0
    
    if prev_lives > 0:
        lives = prev_lives - 1
    else:
        lives = prev_lives
    
    num = current_game_num
    print(f"in hit current game num {current_game_num}")
    
    #sending in hit
    path = "random{}/{}.json".format(num,unique)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join,
        "game_played": game_played,
        "lives": "X"}   

    print("Writing {} to {}".format(data, path))
    
    response1 = authed_session.put(db+path, json=data)
    
    #sending life update
    path = "random{}/{}.json".format(num,i_d)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join,
        "game_played": game_played,
        "lives": lives}
    
    response2 = authed_session.put(db+path,json=data)
    response_check(response2)
    
    winner_check = checking_winner(current_game_num)
    var_list[3] = winner_check
    
def send_swoosh(game_id, max_num):
    
    
    import uuid
    unique = uuid.uuid4()
    i_d = game_id
    hit = 0
    swoosh = 1
    join = 0
    game_played = 0
    
    
    num = max_num 

    print(max_num)
    
    #send(num,i_d,hit,swoosh,join,uuid)
    path = "random{}/{}.json".format(num,unique)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join,
        "game_played": game_played,
        "lives": "X"}    #format of the data you are delivering to table

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
    print(game_tables)
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
    print(my_response[f'{recent_game}'])
    try:
        game_played_check = my_response[f'{recent_game}']['0']['game_played'] #time most recent game_play was initialised
        print(game_played_check)
    except TypeError:
        game_played_check = my_response[f'{recent_game}'][0]['game_played']
        print(game_played_check)
        
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
    lives = 3
    #num = int(game_tables[-1][-1]) + 1
    num = max_num + 1
    print(max_num)
    
    # global current_game_num
    current_game_num = num
    var_list[1] = current_game_num
    
    print(f"game number is {current_game_num}")
    #send(num,i_d,hit,swoosh,join,uuid)
    path = "random{}/{}.json".format(num,i_d)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join,
        "game_played": game_played,
        "lives":lives}    #format of the data you are delivering to table

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
    lives = 3

    num = max_num
    print(num)
    
    global current_game_num
    current_game_num = num
    
    var_list[1] = current_game_num
    
    print(f"game number from join func is {current_game_num}")
    
    path = "random{}/{}.json".format(num,i_d)
    data = {"id":i_d,
        "time":time.time(),
        "hit": hit,
        "swoosh" : swoosh,
        "joining": join,
        "game_played": game_played,
        "lives": lives}    #format of the data you are delivering to table

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
def initialise_game_play_not_w_time(game_played,game_tables,max_num,game_status,create_game):
    print("in initialise game play not w time ")
    
    
    if (game_played == 1) and (game_status == 0 or game_status == 2) and (create_game == 1): #the most recent game has already been played but no game is currently playing
        #make new table with index number greater tha most recent table in database and put in one entry (0th entry)
        init_new_game_play_check(game_tables,max_num) #this function needs to have value for game_played field so that it can be read
        player_i_d = 0
        game_status = 2
        var_list[0] = game_status
        current_game_num = max_num + 1
        var_list[1] = current_game_num
        return 0
    elif (game_played == 0) & (game_status == 0 or game_status == 2 ) & (create_game == 1):
        #join this table as a player
        join_new_game_play_check(game_tables,max_num)
        player_i_d = 1
        game_status = 2
        var_list[0] = game_status
        current_game_num = max_num
        var_list[1] = current_game_num
        return 1
    else:
        player_i_d = -1 # when player id is -1 means player cannot join -- flash an LED
        return -1
        
    
    
    

app: Flask = Flask(__name__)

def main():

    app.run(host="0.0.0.0", port=2000) # Blocking

# Primary page to load

@app.route("/")
def main_page():
    return "Wooo!"

@app.route("/check_status", methods = ['GET'])
def check_game():
    game_status = var_list[0]
    response = make_response(f"""{{"game_status": {game_status}}}""")
    return response

@app.route("/create_game_click", methods = ['GET'])
def create_game():
    create_game = 1
    var_list[2] = create_game
    response = make_response(f"""{{"create_game": {create_game}}}""")
    return response

@app.route("/join", methods = ['GET'] )
def join_game():

    data = request.json
    json_object = json.loads(data)
    hard_id = json_object['hard_id']
    print(hard_id)
    
    
    game_tables = []
    max_num = 0
    path = ".json"
    print("in join game")
    
    
    response = authed_session.get(db+path)
    print(response)
    
    if response.ok:
    
        game_played_check = table_game_played_check(response)
    
        game_status = var_list[0]
        create_game = var_list[2]
        game_played = game_played_check[0]
        print(f"game played is {game_played}")
        game_tables = game_played_check[1]
        print(game_tables)
        max_num = game_played_check[2]
        print(f"max num is {max_num}")
        print(max_num)
        

        init_response = initialise_game_play_not_w_time(game_played,game_tables,max_num,game_status,create_game)
        if init_response == 1:
            player_list.append(init_response)
            player_dict[hard_id] = 1
            print(player_dict)
        elif init_response == 0:
            player_list.append(init_response)
            player_dict[hard_id] = 0
            print(player_dict)
            
        send_back = 0 
        resp = make_response(f"""{{"response": {send_back}}}""")
        print(f"in join game the value of var_list is {var_list}")
        print(f"in join game the value of player_list {player_list}")
        print(f"in join game the value of player dict is {player_dict}")
        return resp
        
    else:
        raise ConnectionError("Could not access database: {}".format(response.text))
    


@app.route("/swoosh", methods = ['GET','POST']) 
def swooshed():
    
    data = request.json
    json_object = dict(data)
    hard_id = json_object['id']
    print((hard_id))
    
    game_id = player_dict[int(hard_id)]
    game_status = var_list[0]
    current_game_num = var_list[1]
    
    print("swooshing")
    print(f"current game num is {current_game_num}")
    
    print(var_list)
    
    if game_status == 1:
        send_swoosh(game_id,current_game_num)
        print("back after swoosh to db")
        response = make_response(f"""{{"i_d": {game_id}}}""")
        return response
    else:
        response = make_response({"no" : "game"})
        return response
    


@app.route("/hit", methods = ['GET', 'POST'] ) 
def hit():
    
    data = request.json
    json_object = json.loads(data)
    hard_id = json_object['hard_id']
    print(hard_id)
    
    game_id = player_dict[hard_id]
    game_status = var_list[0]
    current_game_num = var_list[1]
    print(f"current_game_num is {current_game_num}")
    
    print(var_list)
    
    if game_status == 1:
        send_hit(game_id, current_game_num)
        response = make_response(f"""{{"player_id": {game_id}}}""")
        return response #we return the game status
    else:
        response=make_response({"no" : "game"})
        return response
    
    
@app.route("/play_game", methods = ['GET', 'POST'] ) 
def background_task():
    
    create_game = var_list[2]
    if create_game == 1:
        new_thread = NewThreadedTask()
        new_thread.start()
        print(f"game status after thread has started is now {var_list[0]}")
        # optionally wait for task to complete
        new_thread.join() #game thread has ended
        print(f"game status after thread has ended is now {var_list[0]}")
        print("THREAD MERGED AT END OF THREAD CAST")
        response=make_response({"end":"game"})
        return response
    else:
        return make_response({"not": "play"})
    
@app.route("/calc_stats", methods = ['GET'])
def calcAcc():
    game_status = var_list[0]
    current_game_num = var_list[1]
    #path = f"random{current_game_num}.json"
    
    if game_status == 0:
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
                
                # {0:0.4545, 1:0.3333}
                
                # response {'y':0.4545,'r}
                
                #accuracies['win'] = 'yellow'
            print(accuracies)

            print(player_dict)
            player_dict_inv = {v: k for k, v in player_dict.items()}
            print(player_dict_inv)
            player_accs = {}
            #for key,value in accuracies.items():
                

                # red accuracies and yellow accuracies
                # hid = player_dict_inv[key]
                # colour = colour_dict[hid]
                # player_accs[colour] = value

            player_accs["w"] = winner
            
            response = make_response({"y":45, "r":27, "w":"r"})
            #response = make_response(json.dumps(player_accs))

            print(response)
            return response


        else:
            response = make_response({"no":"response"})
            return response
            raise ConnectionError("Could not access database: {}".format(response.text))
    
    else:
        response = make_response({"0":"0","0":"0","0":"0"})
        return response
            
        
    


        


    
   
    
if __name__ == '__main__':
    main()