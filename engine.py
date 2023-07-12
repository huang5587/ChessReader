import chess
import chess.engine

# def main():


# #     info = engine.analyse(board, chess.engine.Limit(time=0.1))
# #     print("Score:", info["score"])
# # # Score: PovScore(Cp(+20), WHITE)

# #     board = chess.Board("r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 2 4")
# #     info = engine.analyse(board, chess.engine.Limit(depth=20))
# #     print("Score:", info["score"])
# # Score: PovScore(Mate(+1), WHITE)
#     with engine.analysis(board) as analysis:
#         for info in analysis:
#             print(info.get("score"), info.get("pv"))

#             # Arbitrary stop condition.
#             if info.get("seldepth", 0) > 20:
#                 break

#     engine.quit()


def main():
    print("hello world")
    #engine = chess.engine.SimpleEngine.popen_uci("/home/kali/Desktop/chess/stockfish_15_linux_x64")

    engine = chess.engine.SimpleEngine.popen_uci("/home/kali/Desktop/chess/stockfish_15_linux_x64/stockfish_15_src/src/stockfish")
    

    fen = "3q1rk1/p1pb2pn/Pp1p2Np/1P2n2B/3BP3/2Q5/6PP/5RK1 b - - 3 27"
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(depth=20))
    print("Score:", info["score"])
    engine.quit()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()