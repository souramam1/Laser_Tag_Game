import requests,time
import time

#Server IP
SERVER_IP = "146.169.146.162" 

def player_join_req(I_D):

    r = requests.get(url = "http://"+SERVER_IP+":2000/join", json=(f"""{{"hard_id": {I_D}}}"""), timeout=0.8)
    print(r)
    print(r.json())
    my_resp = dict(r.json())
    resp = my_resp["response"]
    print(resp) 
    if resp == -1:
        return 1
    else:
        return 0 
     
    
def check_status():
    r = requests.get(url = "http://"+SERVER_IP+":2000/check_status", timeout=0.5)
    print(r)
    print(r.json())
    my_resp = dict(r.json())
    resp = my_resp['game_status']
    return resp
    
def hit():
    r = requests.get(url = "http://"+SERVER_IP+":2000/hit", json = ({"i_d" : "0"}), timeout=0.5)
    print(r)
    print(r.json())
    my_resp = dict(r.json())
    print(my_resp)
    
    