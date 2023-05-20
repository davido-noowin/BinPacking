#!/bin/sh
# runs ff, ffd, bf, bfd

# ff
python benchmark.py 8192 --algorithm "first_fit"

# ffd
python benchmark.py 8192 --algorithm "first_fit_decreasing"

# bf
python benchmark.py 16384 --algorithm "best_fit"
python benchmark.py 16384 --algorithm "best_fit"

# bffd
python benchmark.py 16384 --algorithm "best_fit_decreasing"
python benchmark.py 16384 --algorithm "best_fit_decreasing"