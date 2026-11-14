# tiny-chess-4k

A chess engine in at most 4,096 bytes of Python, entered in make.fun's
`tiny-chess-01` bounty.

`main.py` is the whole engine: a 0x88 board, move generation, a tapered PeSTO
evaluation with king safety and mobility, and a principal-variation search with
a transposition table, null-move pruning, late-move reductions and a quiescence
search. It searches to a fixed node budget, never a clock, so a replayed trial
makes exactly the same moves.

Python 3.13, standard library only.

## Run it

The engine talks to the grader's env at `$MAKEFUN_ENV_URL`:

```sh
MAKEFUN_ENV_URL=http://127.0.0.1:8080 python3 main.py
```

`src.py` is the readable development source and is not committed; `main.py` is
the compact entry that counts against the size cap.
