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


@app.route("/")
def hello_world():
    return "Hello, World!"

@app.route ("/moves", methods = ['POST'])
def recieve_game_moves():
    data = request.get_json(force=False, silent=False, cache=True)
    print(data)
    mList = data['moves']
    #print("virgin list", mList)
    mList = mList.split("_")
    #print("splitted list", mList)
    setMoves(mList[-1])
    print("Latest Move", mList[-1])
    socketio.emit('moves', mList[-1]) #returns latest move

    return jsonify(dict(message='ok')), 200

@app.route ("/moves", methods = ['GET'])
def print_test():
    return "test test"

@app.route ("/test", methods =['POST'] )
def test_connection():
    data = request.get_json(force=False, silent=False, cache=True)
    print(data)
    # mList = data['moves']
    # #print("virgin list", mList)
    # mList = mList.split("_")
    # #print("splitted list", mList)
    # setMoves(mList[-1])
    # return jsonify({"result": mList[-1]})
    # return mList([-1]) 
    # socketio.emit('moves', mList[-1]) #returns latest move

    if 'moves' in data:
        mList = data['moves']
        mList = mList.split("_")
        setMoves(mList[-1])
        
        return jsonify({"result": mList[-1]})  # Return JSON response
    
    return jsonify({"error": "moves key not found"})  # Return JSON response for error

if __name__ == '__main__':
    move_reciever.start()
    print("running flask server")
    socketio.run(app, host="0.0.0.0", port=8080, allow_unsafe_werkzeug=True, debug=True)
    
