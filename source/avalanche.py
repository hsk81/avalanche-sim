#!/usr/bin/env python
from numpy.random import default_rng
from numpy import abs, array, zeros

import argparse
import json
import numpy
import sys

def avalanche(
    pop_size: int, pop_weights: array,
    max_round: int, max_sample: int, min_sample: int,
    quorum_rate: float, error_share: float
) -> array:
    """
    Simulates for the provided number of `max_round`, the given
    `pop_size` and `max_sample` the *Avalanche* process,  where
    all sample sizes in range of [ `min_sample`, `max_sample` ]
    are considered. A matrix `m` for each round and sample size
    is then returned.

    The `error-share` is the percentage of population, which is
    malicious towards the network attempting to flip peer nodes
    w/o actually following the consensus rules.
    """
    m = zeros(shape=(max_round, max_sample))
    for s in range(min_sample, max_sample + 1):

        p = population(pop_size)
        for r in range(max_round):

            p += errors(pop_weights, error_share); p %= 2 # xor
            m[r, s - 1] = numpy.sum(pop_weights*p) # consensus
            p = resample(p, pop_weights, s, quorum_rate)

    return m

def population(pop_size: int) -> array:
    """
    Returns a uniformly sampled population for given `pop_size`
    where a value of `0` represents *yellow* and a value of `1`
    *red* cards.
    """
    return prg.integers(0, 2, size=pop_size)

def errors(ws: array, share=0.0) -> array:
    """
    Returns a stake-weighted population of adverserial members,
    with `share` being the percentage of total weights.
    """
    return ws.cumsum() < share

def resample(
    p: array, ws: array, size: int, q_rate: float) -> array:
    """
    Make a random choice of a sample `size` (from a given array
    `p`) for *each* element within the array `p`. Then for each
    sample determine, if the q-majority of the sample indicates
    *red* (i.e. `1`) or *yellow* (i.e. `0`) cards.  However, if
    there is *no* q-majority (i.e. tie) within the sample, then
    do nothing.
    """
    ps = prg.choice(p, size=(size, p.size), p=ws).sum(axis=0)
    eq, gt = ps == q_rate * size, ps > q_rate * size

    return p * eq + gt

def weights(pop_size: int, distribution: str) -> array:
    """
    Returns various weight distributions (ie validator stakes).
    """
    def norm(ws):
        return numpy.sort(ws) / ws.sum()
    if distribution == 'cauchy':
        return norm(abs(prg.standard_cauchy(pop_size)))
    elif distribution == 'exponential':
        return norm(prg.standard_exponential(pop_size))
    elif distribution == 'gamma':
        _, shape = distribution.split('-')
        return norm(prg.standard_gamma(float(shape), pop_size))
    elif distribution == 'normal':
        return norm(abs(prg.standard_normal(pop_size)))
    elif distribution.startswith('pareto'):
        _, alpha = distribution.split('-')
        return norm(prg.pareto(float(alpha), pop_size))
    elif distribution == 'uniform':
        return norm(prg.uniform(0, 1.0, pop_size))
    else:
        return norm(numpy.ones(pop_size))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Produces the Avalanche simulation matrix '
                    '[max_round x max_sample]')
    parser.add_argument('-p', '--population',
        type=int, help='population size'
        ' (default: %(default)s)', default=10000)
    parser.add_argument('-d', '--distribution', choices=[
        'cauchy', 'exponential', 'normal', 'uniform', 'equal',
        'pareto-3', 'pareto-2', 'pareto-1', 'pareto-0.5',
        'gamma-3', 'gamma-2', 'gamma-1', 'gamma-0.5'],
        type=str, help='stake distribution'
        ' (default: %(default)s)', default='uniform')
    parser.add_argument('-R', '--max-round',
        type=int, help='maximum number of rounds'
        ' (default: %(default)s)', default=20)
    parser.add_argument('-s', '--min-sample',
        type=int, help='minimum sample size '
        ' (default: %(default)s)', default=1)
    parser.add_argument('-S', '--max-sample',
        type=int, help='maximum sample size '
        ' (default: %(default)s)', default=20)
    parser.add_argument('-q', '--quorum-rate',
        type=float, help='quorum rate'
        ' (default: %(default)s)', default=0.70)
    parser.add_argument('-e', '--error-share',
        type=float, help='error share in [0.0, 0.5)'
        ' (default: %(default)s)', default=0.00)
    parser.add_argument('--random-seed',
        type=int, help='random generator seed'
        ' (default: %(default)s)', default=None)

    args = parser.parse_args()
    prg = default_rng(args.random_seed)

    m = avalanche(
        args.population, weights(args.population, args.distribution),
        args.max_round, args.max_sample, args.min_sample,
        args.quorum_rate, args.error_share)
    numpy.savetxt(
        sys.stdout, m, header=json.dumps(vars(args)))
