import requests,time
import time




#Server IP
SERVER_IP = "146.169.146.162" 
q = 0
def start_game():

    r = requests.get(url = "http://"+SERVER_IP+":2000/play_game", timeout=0.8)
    print(r)
    print(r.json())
    my_resp = dict(r.json())
    print(my_resp) 
    
s_time = time.time()

    
while time.time() - s_time <= 1000:
    
    if q == 0:
        start_game()
        q = 1

