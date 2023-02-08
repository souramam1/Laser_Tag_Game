from flask import Flask, request, make_response
import os
import signal

app: Flask = Flask(__name__)

def main():

    app.run(host="0.0.0.0", port=2000) # Blocking

# Primary page to load

@app.route("/")
def main_page():
    return "Wooo!"

@app.route("/join", methods = ['GET'] )
def join_game():
    resp = make_response('{"body": "text"}')
    return resp
    
if __name__ == '__main__':
    main()