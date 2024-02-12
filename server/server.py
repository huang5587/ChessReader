"""
server.py
    This is the main file for the chessReader backend. 

    The ChessServer class has the following key features:
        - websocket connecting to frontend client
        - integration with a postgreSQL database to store games persistently.
        - a moveReciever instance, which handles the engine analysis. See pyChess.py for the code. 
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
        #init vars
        self.app = app
        self.socketio = socketio
        self.Q = Queue()
        self.move_reciever = moveReciever(self.Q, self.socketio)
        self.moveList = []

        #init psql vars
        self.psql_url = urlparse(os.environ.get("DATABASE_URL"))
        self.db_config = {
            "user": self.psql_url.username,
            "password": self.psql_url.password,
            "host": self.psql_url.hostname,
            "port": self.psql_url.port,
            "database": self.psql_url.path[1:],
        }

        #register routes
        self.app.route('/moves', methods=['POST'])(self.receive_game_moves)
        self.app.route('/')(self.hello_world)

    #helper function declarations
    def run(self):
        self.move_reciever.start()
        print("running flask server")
        self.socketio.run(self.app, host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True, debug=True)

    #saveMoves() connects to the psql database and saves the complete game into the database.
    def saveMoves(self, game_moves):
        conn = psycopg2.connect(**self.db_config)
        try:
            with conn.cursor() as cursor:
                #check if games table exists, and create it if not. 
                cursor.execute(f"CREATE TABLE IF NOT EXISTS games (ID SERIAL PRIMARY KEY, moves TEXT);")

                # Save game into table
                cursor.execute("INSERT INTO games (moves) VALUES (%s)", (game_moves,))
            conn.commit()
        finally:
            conn.close()
    
    #define route handlers
    def hello_world(self):
        return "Server is Online"
    
    #receive_game_moves() is a route handler. it is executed when the /moves route is active. 
    def receive_game_moves(self):
        data = request.get_json(force=False, silent=False, cache=True)
        self.moveList = data['moves']
        self.moveList = self.moveList.split("_")

        #pattern represents "any number - any number". It is meant to capture the scores output by chess.com when a game ends. 
        pattern = re.compile(r'\d+-\d+')

        #check if game is over.
        if pattern.fullmatch(self.moveList[-1]):

            #save game in psql database
            move_string = ",".join(self.moveList)
            self.saveMoves(move_string)

            #reset moveList
            self.moveList = []
            self.socketio.emit('gameover')
        else:
            #add move to Q so the engine can conduct analysis. 
            self.Q.put(self.moveList[-1])
            self.socketio.emit('moves', self.moveList[-1]) #returns latest move

        return jsonify(dict(message='ok')), 200

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, resources={r"/*":{"origins":"*"}})

    socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)

    cs = ChessServer(app, socketio)
    cs.run()
