from concurrent.futures.thread import _worker
from queue import Queue as Q
import chess
import chess.engine
import threading

"""
    This class exists to process and analyze moves using the python chess library.

"""

class moveReciever(threading.Thread):
    def __init__(self, workQ: Q, socketio):
        super().__init__()
        self.workQ = workQ
        self.socketio = socketio
        self.engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
        self.daemon = True
        self.board = chess.Board()

    def run(self):
        print("Move Reciever running ...")
        #make move on board
        # board = chess.Board()
        
        while True: #loops until termination
            #retrieve moves from Q
            work = self.workQ.get()    
            try:
                #make moves on board
                self.board.push_san(work)

                engine_moves = self.engine.analyse(self.board, chess.engine.Limit(time=0.1), multipv=3)

                payload = []
            
                #strip analysis lines from info object, emit to server
                for x in range(0,3):
                    analList = []
                    for i in range(0, len(engine_moves[x]['pv'])):
                        analList.append(str(engine_moves[x]['pv'][i]))
                    payload.append(analList)

                self.socketio.emit('analysis', payload) #payload is a list, each index is a list of engine moves.

            except Exception as error:
                print("Move Reciever", error)

    def reset(self):
        self.board = chess.Board()