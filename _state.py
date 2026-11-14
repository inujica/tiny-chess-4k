"""Check that make/unmake leaves the incremental state equal to a rebuild. Not part of the entry."""
import sys

sys.path.insert(0, "/root/makefun/chess/build")
import src


def fen_of(pos):
    rows = []
    for r in range(7, -1, -1):
        row = ""
        n = 0
        for f in range(8):
            p = pos.b[r * 16 + f]
            if not p:
                n += 1
                continue
            if n:
                row += str(n)
                n = 0
            t = " pnbrqk"[p & 7]
            row += t.upper() if p >> 3 == 0 else t
        if n:
            row += str(n)
        rows.append(row)
    c = ""
    for bit, ch in ((1, "K"), (2, "Q"), (4, "k"), (8, "q")):
        if pos.castle & bit:
            c += ch
    ep = "-" if pos.ep < 0 else "abcdefgh"[pos.ep & 7] + "12345678"[pos.ep >> 4]
    return "/".join(rows) + f" {'w' if pos.side == 0 else 'b'} {c or '-'} {ep} 0 1"


FENS = [
    "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1",
    "r1bqkb1r/pppp1ppp/2n2n2/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 4 4",
    "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1",
    "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1",
    "rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8",
]

bad = 0
seen = 0


def walk(pos, depth):
    global bad, seen
    fresh = src.Position().set_fen(fen_of(pos))
    if (fresh.hash, fresh.mg, fresh.eg, fresh.phase, fresh.pawns, fresh.bishops) != \
       (pos.hash, pos.mg, pos.eg, pos.phase, pos.pawns, pos.bishops):
        print("MISMATCH at", fen_of(pos), pos.side)
        print("  hash", hex(pos.hash), hex(fresh.hash))
        print("  mg", pos.mg, fresh.mg, "eg", pos.eg, fresh.eg)
        print("  phase", pos.phase, fresh.phase)
        print("  pawns", pos.pawns, fresh.pawns)
        print("  bishops", pos.bishops, fresh.bishops)
        bad += 1
        return
    seen += 1
    if depth == 0:
        return
    for m in pos.legal():
        pos.make(m)
        walk(pos, depth - 1)
        pos.unmake()


for f in FENS:
    walk(src.Position().set_fen(f), 3)
print(f"checked {seen} nodes, {bad} mismatches")
