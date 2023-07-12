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
        self.engine = chess.engine.SimpleEngine.popen_uci("/home/kali/Desktop/chess/stockfish_15_linux_x64/stockfish_15_src/src/stockfish")
        self.daemon = True
        self.board = chess.Board()

    def run(self):
        #make move on board
        board = chess.Board()
        
        while True: #loops until termination
            #retrieve moves from Q
             work = self.workQ.get()    
             try:
                #make moves on board
                board.push_san(work)
                info = self.engine.analyse(board, chess.engine.Limit(time=0.1), multipv=3)

                payload = []
                
                print("info ting 1:" ,info[0]['pv']) #output [Move.from_uci('d4e5'), Move.from_uci('b8c6')]
                print("info ting 2:" ,info[1]['pv'])
                print("info ting 3:" ,info[2]['pv'])

                #strip analysis lines from info object, emit to server
                for x in range(0,3):
                    analList = []
                    for i in range(0, len(info[x]['pv'])):
                        analList.append(str(info[x]['pv'][i]))
                    print("anallist", analList)
                    payload.append(analList)

                self.socketio.emit('analysis', payload) #payload is a list, each index is a list of engine moves.
                print("payload:", payload)

                """
                {'string': 'NNUE evaluation using nn-6877cd24400e.nnue enabled',
                 'depth': 11,
                 'seldepth': 15,
                'multipv': 1,
                'score': PovScore(Cp(+35), WHITE),
                'nodes': 15737,
                'nps': 135663,
                'tbhits': 0
                'time': 0.116, 
                'pv': [Move.from_uci('d2d4'), Move.from_uci('d7d5'), Move.from_uci('e2e4'), Move.from_uci('d5e4'), Move.from_uci('d4d5'), Move.from_uci('c6b8'), Move.from_uci('c3e4'), Move.from_uci('e7e5'), Move.from_uci('f2f4'), Move.from_uci('g8f6'), Move.from_uci('e4f6'), Move.from_uci('d8f6')]}

                """
             except Exception as error:
                print("Move Reciever", error)
