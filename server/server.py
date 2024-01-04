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

import chess
import chess.engine

print("hello hello")
# app = create_app()
# CORS(app, resources={r"/*":{"origins":"*"}})
app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)

Q = Queue()
move_reciever = moveReciever(Q, socketio)
global moveList 
moveList = []
global curMove
curMove = []
#engine = chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish")
def setMoves(inputMoves):
    moveList = inputMoves
    Q.put(inputMoves)
    print("move set as: ", moveList)

# def get_cur_move(inputMoves = list):
#     if not curMove:
#         curMove = inputMoves[0]
#         print("cur", curMove)
#     else: 
#         curMove = inputMoves[-1]
#         print("cur", curMove)
#     return curMove

@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route ("/moves", methods = ['POST'])
def recieve_game_moves():
    data = request.get_json(force=False, silent=False, cache=True)
    mList = data['moves']
    #print("virgin list", mList)
    mList = mList.split("_")
    #print("splitted list", mList)
    setMoves(mList[-1])
    socketio.emit('moves', mList[-1]) #returns latest move

    return jsonify(dict(message='ok')), 200

@app.route ("/test", methods =['GET'] )
def test_connection():
    print( "test success")
    return "recieved", 200

if __name__ == '__main__':
    move_reciever.start()
    print("running flask server")
    socketio.run(app, host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True)
    
