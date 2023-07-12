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

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

socketio = SocketIO(app, cors_allowed_origins="*", async_mode=None)

Q = Queue()
move_reciever = moveReciever(Q, socketio)
global moveList 
moveList = []
scopeTest = "hello scope works"
global curMove
curMove = []
c=[]
#engine = chess.engine.SimpleEngine.popen_uci("/usr/bin/stockfish")
def setMoves(inputMoves):
    moveList = inputMoves
    Q.put(inputMoves)
    print("move set as: ", moveList)

def count(c):
    c.append("1")
    print("move counter: ", len(c))

def fun():
    print("function works")
    print("move list is: ", moveList)

# def get_cur_move(inputMoves = list):
#     if not curMove:
#         curMove = inputMoves[0]
#         print("cur", curMove)
#     else: 
#         curMove = inputMoves[-1]
#         print("cur", curMove)
#     return curMove

@app.before_first_request
def before_first_request():
    move_reciever.start()

@app.route ("/moves", methods = ['POST'])
def recieve_game_moves():
    data = request.get_json(force=False, silent=False, cache=True)
    mList = data['moves']
    #print("virgin list", mList)
    mList = mList.split("_")
    #print("splitted list", mList)
    setMoves(mList[-1])
    socketio.emit('moves', mList[-1]) #returns latest move
    # print(scopeTest)
    # fun()
    return jsonify(dict(message='ok')), 200

@app.route ("/test", methods =['GET'] )
def test_connection():
    print( "test success")
    return "recieved", 200

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0")
    
