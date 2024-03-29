from flask import Flask, request, make_response
import threading
import os
import signal
import json
import requests,time,random,uuid
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from join_db_flask import access_db

# winner = None #"r" or "y"

class NewThreadedTask(threading.Thread):
    #this is where the game play will be defined 

    game_status: int
    current_game_num: str
    create_game: int
    winner_check = False

    server: any

    def __init__(self, server: any):
         super(NewThreadedTask, self).__init__()
         self.server = server
         
    def run(self):
        s_time = time.time()
        print(F"WINNER CHECK IS {self.server.winner_check}")
        while ((time.time()-s_time) <= 40) and (self.server.winner_check == 0):
            
            if (time.time()%10 == 0):
                print(f"winner check is {self.server.winner_check}")
            
            self.server.game_status = 1
            self.server.create_game = 0
   
        print('End of threaded game while loop')
        self.game_played_update(self.server.current_game_num)
        self.server.game_status = 0
        print("End of end of game changes")
        self.server.player_list = []
        self.server.player_dict = {}
        self.server.winner_list = []
        return

class MagicTagServer:

    ### DATABASE ###

    database = {
        "db" : "https://laser-tag-testing-default-rtdb.europe-west1.firebasedatabase.app/",
        "keyfile" : "laser-tag-testing-firebase-adminsdk-6h09n-67f1530174.json",
        "scopes" : [
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/firebase.database"
        ]
    }

    authed_session = AuthorizedSession(service_account.Credentials.from_service_account_file(database["keyfile"], scopes=database["scopes"]))

    game_status = 0
    current_game_num = 'X'
    create_game = 1
    winner_check = False

    winner_list = []
    player_list = []

    player_dict = {}
    colour_dict = {22:'y', 33:'r'}

    def __init__(self):
        print("temp")

    def response_check(self, response):
        if response.ok:  #error checking
            print("Created new node named {}".format(response.json()["id"]))
        else:
            raise ConnectionError("Could not write to database: {}".format(response.text))

    def checking_winner(self):
        print("inside checking winner!!!!!!")
        #query database for win
        print(self.player_list)
        for players in self.player_list:
            print(f"inside for loop in checking winner, player is {players}")
            
            path = "random{}/{}.json".format(self.current_game_num, players)
            response = (self.authed_session.get(self.database["db"]+path))
            prev_lives = dict(response.json())['lives']
            self.winner_list.append(prev_lives)
            losers = self.winner_list.count(0)
        
        print(self.winner_list)  

        if len(self.player_list) - losers == 1:
            print("returning winner check is 1 from checking winner function")
            return True
        else:
            print("returning winner check is 0 from checking winner function") 
            return False

    ### IS THIS USEFUL? ###
    def game_played_update(self):
        
        i_d = 0
        hit = 0
        swoosh = 0
        join = 0
        game_played = 1

        print("int game update after game end")
        
        path = "random{}/0.json".format(self.current_game_num)
        data = {"id":i_d,
            "time":time.time(),
            "hit": hit,
            "swoosh" : swoosh,
            "joining": join,
            "game_played": game_played}    #format of the data you are delivering to table
        
        response = self.authed_session.put(self.database["db"] + path, json=data)  #put creates new nodes
        
        if response.ok:
            print("Ok")
        else:
            raise ConnectionError("Could not write to database: {}".format(response.text))
        time.sleep(1)

        print("Writing {} to {}".format(data, path))
        
    def send_hit(self, game_id):
        print("top of send hit")
    
        unique = uuid.uuid4()
        
        path = "random{}/{}.json".format(self.current_game_num,game_id)
        response = (self.authed_session.get(self.database["db"]+path))
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
        
        num = self.current_game_num
        print(f"in hit current game num {self.current_game_num}")
        
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
        
        # response1 = authed_session.put(db+path, json=data)
        
        #sending life update
        path = "random{}/{}.json".format(num,i_d)
        data = {"id":i_d,
            "time":time.time(),
            "hit": hit,
            "swoosh" : swoosh,
            "joining": join,
            "game_played": game_played,
            "lives": lives}
        
        response2 = self.authed_session.put(self.database["db"]+path,json=data)
        self.response_check(response2)
        
        self.winner_check = self.checking_winner(self.current_game_num)
        
    def send_swoosh(self, game_id, max_num):
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
        response = self.authed_session.put(self.database["db"]+path, json=data)
        #response_check(response)
        
    def max_table_num(self, game_tables):
        table_nums = []
        for word in game_tables:
            int_num = int(word.split("random")[1])
            table_nums.append(int_num)
            recent_num = max(table_nums)
            
        return recent_num
        

    def table_time_made(self, response): #time creation definition #change this to check if the game_play entry in 0th row of most recent table is 0
        
        my_response = dict(response.json())
        tables = my_response.keys()
        game_tables = []
        
        for item in tables:
            if item.find("random") != -1: #this will be changed to "gameplay" for the actual simulation
                game_tables.append(item)
                print("table found : checking time creation!")
            
        #recent_game = game_tables[-1]
        print(game_tables)
        mx = self.max_table_num(game_tables)
        recent_game = "random"+f"{mx}" #change random for game_tables
        print(recent_game)
        
        t_created = my_response[f'{recent_game}'][0]['time'] #time most recent game_play was initialised
        return t_created, game_tables, mx

    def table_game_played_check(self, response): #time creation definition #change this to check if the game_play entry in 0th row of most recent table is 0
        
        my_response = dict(response.json())
        tables = my_response.keys()
        game_tables = []
        
        for item in tables:
            if item.find("random") != -1: #this will be changed to "gameplay" for the actual simulation
                game_tables.append(item)
                print("table found : checking time creation!")
            
        #recent_game = game_tables[-1]
        mx = self.max_table_num(game_tables)
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

    def init_new_game(self, game_tables,max_num): #if time limit to join game has been exceeded new game is started
        
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
        response = self.authed_session.put(self.database["db"]+path, json=data)
        self.response_check(response)

    def init_new_game_play_check(self, game_tables,max_num): #if time limit to join game has been exceeded new game is started
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
        self.current_game_num = num
        
        print(f"game number is {self.current_game_num}")
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
        response = self.authed_session.put(self.database["db"]+path, json=data)
        self.response_check(response)

    def join_new_game(self, game_tables,max_num):
        
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
        response = self.authed_session.put(self.database["db"]+path, json=data)
        self.response_check(response)
        
    def join_new_game_play_check(self, game_tables,max_num):
        print("in join_new game_play")
        i_d = 1
        hit = 0
        swoosh = 0
        join = 1
        game_played = 0
        lives = 3

        num = max_num
        print(num)

        self.current_game_num = num
        
        print(f"game number from join func is {self.current_game_num}")
        
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
        response = self.authed_session.put(self.database["db"]+path, json=data)
        self.response_check(response)

    def initialise_game_play(self, time_check,game_tables,max_num):
        
        if time.time() - time_check >= 30:
            #make new table with index number greater than most recent table in database and put in one entry (0th entry)
            self.init_new_game(game_tables,max_num)
            player_i_d = 0
        else:
            #join this table as a player
            self.join_new_game(game_tables,max_num)
            player_i_d = 1
        
        return player_i_d

    #This function is the new one i added
    def initialise_game_play_not_w_time(self, game_played,game_tables,max_num,game_status,create_game):
        print("in initialise game play not w time ")
        
        if (game_played == 1) and (game_status == 0 or game_status == 2) and (create_game == 1): #the most recent game has already been played but no game is currently playing
            #make new table with index number greater tha most recent table in database and put in one entry (0th entry)
            self.init_new_game_play_check(game_tables,max_num) #this function needs to have value for game_played field so that it can be read
            player_i_d = 0
            self.game_status = 2
            self.current_game_num = max_num + 1
            return 0
        elif (game_played == 0) & (game_status == 0 or game_status == 2 ) & (create_game == 1):
            #join this table as a player
            self.join_new_game_play_check(game_tables,max_num)
            player_i_d = 1
            self.game_status = 2
            self.current_game_num = max_num
            return 1
        else:
            player_i_d = -1 # when player id is -1 means player cannot join -- flash an LED
            return -1
    
    def check_status(self):
        return make_response(f"""{{"game_status": {self.game_status}}}""")

    def make_game(self):
        self.create_game = 1
        return make_response(f"""{{"create_game": {self.create_game}}}""")

    def game_join(self, request):
        hard_id = json.loads(request.json)['hard_id']

        game_tables = []
        max_num = 0
        path = ".json"
        print("in join game")

        response = self.authed_session.get(self.database["db"]+path)

        if response.ok:
            game_played_check = self.table_game_played_check(response)
        
            game_played = game_played_check[0]
            print(f"game played is {game_played}")
            game_tables = game_played_check[1]
            print(game_tables)
            max_num = game_played_check[2]
            print(f"max num is {max_num}")
            print(max_num)
            

            init_response = self.initialise_game_play_not_w_time(game_played,game_tables,max_num,self.game_status,create_game)
            if init_response == 1:
                self.player_list.append(init_response)
                self.player_dict[hard_id] = 1
                print(self.player_dict)
            elif init_response == 0:
                self.player_list.append(init_response)
                self.player_dict[hard_id] = 0
                print(self.player_dict)

            return make_response(f"""{{"response": {0}}}""")
        else:
            raise ConnectionError("Could not access database: {}".format(response.text))

    def swooshed(self, request):
        
        hard_id = dict(request.json)['id']

        game_id = self.player_dict[int(hard_id)]
        
        print("swooshing")
        print(f"current game num is {self.current_game_num}")
        
        if self.game_status == 1:
            self.send_swoosh(game_id,self.current_game_num)
            print("back after swoosh to db")
            return make_response(f"""{{"i_d": {game_id}}}""")
        else:
            return make_response({"no" : "game"})

    def hit(self, request):
        hard_id = json.loads(request.json)['hard_id']
        
        game_id = self.player_dict[hard_id]
        print(f"current_game_num is {self.current_game_num}")
        
        if self.game_status == 1:
            self.send_hit(game_id, self.current_game_num)
            return make_response(f"""{{"player_id": {game_id}}}""")
        else:
            return make_response({"no" : "game"})

    def bg_task(self):
        if self.create_game == 1:
            new_thread = NewThreadedTask(self)
            new_thread.start()
            # optionally wait for task to complete
            new_thread.join() #game thread has ended
            return make_response({"end":"game"})
        else:
            return make_response({"not": "play"})

    def calc_stats(self):
        if self.game_status == 0:
            path = "statistics_test.json"

            response = (self.authed_session.get(self.database["db"]+path))
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

                print(self.player_dict)
                player_dict_inv = {v: k for k, v in self.player_dict.items()}
                print(player_dict_inv)
                player_accs = {}
                #for key,value in accuracies.items():
                    

                    # red accuracies and yellow accuracies
                    # hid = player_dict_inv[key]
                    # colour = colour_dict[hid]
                    # player_accs[colour] = value

                player_accs["w"] = self.winner
                
                response = make_response({"y":45, "r":27, "w":"r"})
                #response = make_response(json.dumps(player_accs))

                print(response)
                return response


            else:
                return make_response({"no":"response"})
                # raise ConnectionError("Could not access database: {}".format(response.text))
        
        else:
            return make_response({"0":"0","0":"0","0":"0"})


        

app: Flask = Flask(__name__)

server = MagicTagServer()

def main():
    app.run(host="0.0.0.0", port=2000) # Blocking

# Primary page to load

@app.route("/")
def main_page():
    return "Wooo!"

@app.route("/check_status", methods = ['GET'])
def check_game():
    return server.check_status()

@app.route("/create_game_click", methods = ['GET'])
def create_game():
    return server.make_game()

@app.route("/join", methods = ['GET'] )
def join_game():
    return server.game_join(request)

@app.route("/swoosh", methods = ['GET','POST']) 
def swooshed():
    return server.swooshed(request)

@app.route("/hit", methods = ['GET', 'POST'] ) 
def hit():
    return server.hit(request)
    
@app.route("/play_game", methods = ['GET', 'POST'] ) 
def background_task():
    return server.bg_task()
    
@app.route("/calc_stats", methods = ['GET'])
def calcAcc():
    return server.calc_stats()

if __name__ == '__main__':
    main()