"""Assert make/unmake restores every incremental field exactly. Not part of the entry."""
import sys

sys.path.insert(0, "/root/makefun/chess/build")
import src

FENS = [
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
    "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
    "8/8/8/K1Pp3r/8/8/8/8 w - d6 0 1",
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R b KQkq - 0 1",
]

bad = 0
total = 0


def snap(p):
    return (list(p.b), p.side, p.castle, p.ep, p.half, p.mg, p.eg, p.phase,
            list(p.kings), p.hash, list(p.pawns), list(p.bishops))


def walk(pos, depth):
    global bad, total
    if depth == 0:
        return
    for m in pos.legal():
        before = snap(pos)
        pos.make(m)
        walk(pos, depth - 1)
        pos.unmake()
        after = snap(pos)
        total += 1
        if before != after:
            bad += 1
            names = ("b", "side", "castle", "ep", "half", "mg", "eg", "phase",
                     "kings", "hash", "pawns", "bishops")
            print("NOT RESTORED after", src.uci(m), [n for n, x, y in zip(names, before, after) if x != y])
            for n, x, y in zip(names, before, after):
                if x != y and n in ("pawns", "bishops", "mg", "eg", "phase", "hash"):
                    print("   ", n, x, y)
            if bad > 5:
                sys.exit(1)


for f in FENS:
    walk(src.Position().set_fen(f), 4)
print(f"{total} make/unmake pairs, {bad} not restored")
