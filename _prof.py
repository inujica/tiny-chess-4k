import cProfile, pstats, sys, io
sys.path.insert(0, "/root/makefun/chess/build")
import src
pos = src.Position().set_fen("r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4")
eng = src.Engine()
pr = cProfile.Profile()
pr.enable()
eng.think(pos, [pos.hash], 30000)
pr.disable()
s = io.StringIO()
pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(14)
print(s.getvalue())
