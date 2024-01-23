"""
Jun Han Huang
server.py
    -recieves moves from xtension
    -conducts analysis
        -split moves and send enqueue 
    -emits analysis to client. 
"""

from flask import Flask, jsonify, request
from flask_socketio import SocketIO
from flask_cors import CORS
from pyChess import moveReciever
from queue import Queue
from urllib.parse import urlparse

import re
import psycopg2 
import os

print("hello hello")

app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)


#init global vars
Q = Queue()
move_reciever = moveReciever(Q, socketio)
global moveList 
moveList = []


#init db connection
database_url = os.environ.get("DATABASE_URL")
url = urlparse(database_url)

db_config = {
    "user": url.username,
    "password": url.password,
    "host": url.hostname,
    "port": url.port,
    "database": url.path[1:],
}

def setMoves(inputMoves):
    moveList = inputMoves
    Q.put(inputMoves)
    print("move set as: ", moveList)

# Function to insert chess game into the database
def saveMoves(game_moves):
    conn = psycopg2.connect(**db_config)

    #check if DB was just created
    if is_schema_empty(cursor):
        cursor.execute(f"CREATE TABLE games (ID SERIAL PRIMARY KEY, moves TEXT);")
    try:
        with conn.cursor() as cursor:
            # Insert the game_moves into the chess_games table
            cursor.execute("INSERT INTO games (moves) VALUES (%s)", (game_moves,))
        conn.commit()
    finally:
        conn.close()

def is_schema_empty(cursor):
    # Check if the schema is empty by querying the tables in the schema
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables")
    return cursor.rowcount == 0

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route ("/moves", methods = ['POST'])
def recieve_game_moves():
    data = request.get_json(force=False, silent=False, cache=True)
    mList = data['moves']
    mList = mList.split("_")

    #pattern represents "any number - any number". It is meant to capture the scores output by chess.com when a game ends. 
    pattern = re.compile(r'\d+-\d+')

    #game is over
    if pattern.fullmatch(mList[-1]):
        #save game in psql database
        move_string = ",".join(mList)
        saveMoves(move_string)

        #reset moveList
        moveList = []
        socketio.emit('gameover', {})
    else:
        setMoves(mList[-1])
        socketio.emit('moves', mList[-1]) #returns latest move

    return jsonify(dict(message='ok')), 200

@app.route ("/moves", methods = ['GET'])
def print_test():
    if request.method == "OPTIONS":
        # Handle preflight OPTIONS request
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        }
        return "", 204, headers
    else:
        headers = dict(request.headers)
        print("Request Headers:", headers)
        return jsonify(message="Test route")

if __name__ == '__main__':
    move_reciever.start()
    print("running flask server")
    socketio.run(app, host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True, debug=True)
    
