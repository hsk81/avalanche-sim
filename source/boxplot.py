#!/usr/bin/env python
from matplotlib import pyplot as pp
from typing import Tuple, Dict

from numpy import array
from numpy import average as avg
from numpy import std
from numpy import maximum
from numpy import minimum

import argparse
import io
import json
import numpy
import sys

def parse():
    parser = argparse.ArgumentParser(
        description='Plots the Avalanche simulation matrix as boxplots')

    parser.add_argument('-r', '--min-round',
        type=int, help='minimum round'
        ' (default: %(default)s)', default=0)
    parser.add_argument('-R', '--max-round',
        type=int, help='maximum round'
        ' (default: %(default)s)', default=None)
    parser.add_argument('-s', '--min-sample',
        type=int, help='minimum sample size'
        ' (default: %(default)s)', default=None)
    parser.add_argument('-S', '--max-sample',
        type=int, help='maximum sample size'
        ' (default: %(default)s)', default=None)

    return parser.parse_args()

def normalize(m: array, scale: float = 1.0) -> array:

    return scale * maximum(m, 1.0 - m)

def prettify(m: array, scale: float = 1.0) -> array:

    return round(scale * m) / scale

def data(text_io: io.TextIOBase, rounds: int) -> str:

    return ''.join([text_io.readline() for r in range(rounds)])

def read(text_io: io.TextIOBase) -> Tuple[array, Dict]:

    line = text_io.readline()
    meta = json.loads(line[2:])

    ms = []
    while line:
        meta = json.loads(line[2:])
        m = numpy.loadtxt(io.StringIO(data(text_io, meta['max_round'])))
        m = normalize(m, scale=100.0)
        ms.append(m)
        line = text_io.readline()

    return array(ms), meta

def factorize(n: int) -> Tuple[int, int]:

    factors = list(
        filter(lambda i: n % i == 0, range(1, n+1)))
    tuples = sorted([(abs(lhs-rhs), lhs, rhs)
        for lhs in factors for rhs in factors if lhs*rhs == n])

    return tuples[0][1:] if len(tuples) > 0 else (0, 0)

if __name__ == '__main__':

    args = parse()
    ms, meta = read(sys.stdin)

    ms_avg = avg(ms, axis=0)
    ms_std = std(ms, axis=0)

    min_round = args.min_round
    max_round = args.max_round \
        if args.max_round else meta['max_round']
    min_sample = args.min_sample \
        if args.min_sample else meta['min_sample']
    max_sample = args.max_sample \
        if args.max_sample else meta['max_sample']

    sample_v, sample_h = factorize(max_sample - min_sample + 1)
    sample = sample_v * sample_h

    fig, ax = pp.subplots(1, 1)
    fig.suptitle('Avalanche for |P|={0} & Error={1}%'
        .format(meta['population'], 100*meta['error_share'])
        .replace(',', "'"), fontsize=21, y=0.95)

    for s in range(sample):
        idx_sample = min_sample + s - 1

        ax = pp.subplot(sample_h, sample_v, s+1)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        pp.title(' |sample|={0}'.format(idx_sample+1), fontweight="bold", loc='left', pad=-25)
        pp.xlim([0, minimum(ms_avg.shape[0], max_round)])
        pp.xlabel('Rounds [#]')
        pp.ylim([50, 100])
        pp.ylabel('Consensus [%]')

        pp.grid(
            True, 'major', 'y', ls='--', lw=0.5, c='k', alpha=0.61)
        pp.boxplot(
            ms[:,min_round:max_round,idx_sample],
            positions=range(min_round, max_round), notch=True)
        pp.plot(
            range(min_round, max_round),
            ms_avg[min_round:max_round,idx_sample],
            '.:', color='black')

        ax.xaxis.set_major_formatter(
            pp.FuncFormatter(lambda n, _: '{:.0f}'.format(n+1)))
        ax.yaxis.set_major_formatter(
            pp.FuncFormatter(lambda n, _: '{:.2f}%'.format(n)))

    pp.subplots_adjust(hspace=0.35)
    pp.show()
