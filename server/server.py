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

class ChessServer():
    def __init__(self, app, socketio):
        self.app = app
        self.socketio = socketio
        self.Q = Queue()
        self.move_reciever = moveReciever(self.Q, self.socketio)
        self.moveList = []
        self.psql_url = urlparse(os.environ.get("DATABASE_URL"))
        self.db_config = {
            "user": self.psql_url.username,
            "password": self.psql_url.password,
            "host": self.psql_url.hostname,
            "port": self.psql_url.port,
            "database": self.psql_url.path[1:],
        }
        self.count = 0
        #register routes
        self.app.route('/moves', methods=['POST'])(self.receive_game_moves)
        self.app.route('/')(self.hello_world)

    #helper function declarations
    def run(self):
        self.move_reciever.start()
        print("running flask server")
        self.socketio.run(self.app, host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True, debug=True)

    def setMoves(self, latestMove):
        #self.moveList = latestMove
        self.Q.put(latestMove)

    def saveMoves(self, game_moves):
        self.count = self.count + 1
        print("==================== count is: ", self.count)
        conn = psycopg2.connect(**self.db_config)
        try:
            with conn.cursor() as cursor:
                #check if DB was just created
                if self.isSchemaEmpty(cursor):
                    cursor.execute(f"CREATE TABLE games (ID SERIAL PRIMARY KEY, moves TEXT);")

                # Insert the game_moves into the chess_games table
                cursor.execute("INSERT INTO games (moves) VALUES (%s)", (game_moves,))
            conn.commit()
        finally:
            conn.close()
    
    def isSchemaEmpty(self, cursor):
        # Check if the schema is empty by querying the tables in the schema
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables")
        return cursor.rowcount == 0
    
    #route handlers
    def hello_world(self):
        return "Server is Online"
    
    def receive_game_moves(self):
        data = request.get_json(force=False, silent=False, cache=True)
        self.moveList = data['moves']
        self.moveList = self.moveList.split("_")

        #pattern represents "any number - any number". It is meant to capture the scores output by chess.com when a game ends. 
        pattern = re.compile(r'\d+-\d+')

        #game is over
        if pattern.fullmatch(self.moveList[-1]):

            #save game in psql database
            move_string = ",".join(self.moveList)
            self.saveMoves(move_string)

            #reset moveList
            self.moveList = []
            self.socketio.emit('gameover')
        else:
            self.setMoves(self.moveList[-1])
            self.socketio.emit('moves', self.moveList[-1]) #returns latest move

        return jsonify(dict(message='ok')), 200

if __name__ == '__main__':
    #declare vars
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/*":{"origins":"*"}})

    socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)

    cs = ChessServer(app, socketio)
    cs.run()



##############



# def setMoves(self, inputMoves):
#     moveList = inputMoves
#     self.Q.put(inputMoves)
#     print("move set as: ", moveList)

# # Function to insert chess game into the database
# def saveMoves(self, game_moves):
#     conn = psycopg2.connect(**db_config)

#     #check if DB was just created
#     if self.is_schema_empty(cursor):
#         cursor.execute(f"CREATE TABLE games (ID SERIAL PRIMARY KEY, moves TEXT);")
#     try:
#         with conn.cursor() as cursor:
#             # Insert the game_moves into the chess_games table
#             cursor.execute("INSERT INTO games (moves) VALUES (%s)", (game_moves,))
#         conn.commit()
#     finally:
#         conn.close()

# def is_schema_empty(self, cursor):
#     # Check if the schema is empty by querying the tables in the schema
#     cursor.execute("SELECT COUNT(*) FROM information_schema.tables")
#     return cursor.rowcount == 0

# @app.route("/")
# def hello_world():
#     return "Server is Online"

# @app.route ("/moves", methods = ['POST'])
# def recieve_game_moves():
#     data = request.get_json(force=False, silent=False, cache=True)
#     mList = data['moves']
#     mList = mList.split("_")

#     #pattern represents "any number - any number". It is meant to capture the scores output by chess.com when a game ends. 
#     pattern = re.compile(r'\d+-\d+')

#     #game is over
#     if pattern.fullmatch(mList[-1]):
#         #save game in psql database
#         move_string = ",".join(mList)
#         saveMoves(move_string)

#         #reset moveList
#         moveList = []
#         socketio.emit('gameover', {})
#     else:
#         setMoves(mList[-1])
#         socketio.emit('moves', mList[-1]) #returns latest move

#     return jsonify(dict(message='ok')), 200

    
