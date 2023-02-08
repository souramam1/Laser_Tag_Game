from flask import Flask, request, make_response
import os
import signal
import requests,time,random,uuid
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from join_db_flask import access_db

app: Flask = Flask(__name__)

def main():

    app.run(host="0.0.0.0", port=2000) # Blocking

# Primary page to load

@app.route("/")
def main_page():
    return "Wooo!"

@app.route("/join", methods = ['GET'] )
def join_game():
    print("hello world!")
    access_db()
    resp = make_response('{"body": "text"}')
    return resp


    
    
    
if __name__ == '__main__':
    main()