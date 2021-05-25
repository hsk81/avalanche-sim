#!/usr/bin/env python
#######################################################################

from numpy.random import default_rng
from numpy import abs, array, zeros
from typing import Tuple, TextIO

import argparse
import json
import numpy
import sys

#######################################################################
#######################################################################

def avalanche(
    p_weights: array, max_round: int,
    max_sample: int, min_sample: int,
    q_rate: float, e_share: float
) -> array:
    """
    Simulates for the provided number of `max_round`, the given
    `p_weights.size` and `max_sample` an **Avalanche** process,
    where *all* sample sizes in the [`min_sample`,`max_sample`]
    range are simulated for! Then, a matrix for *each* round &&
    sample size is returned.

    The `e-share` is the **percentage** of population, which is
    malicious towards the network attempting to flip peer nodes
    w/o actually following the consensus rules.
    """
    m = zeros(shape=(max_round, max_sample))
    for s in range(min_sample, max_sample + 1):

        p = population(p_weights.size)
        c = counters(p_weights.size)
        for r in range(max_round):

            p += errors(p_weights, e_share); p %= 2 # xor error
            m[r, s - 1] = numpy.sum(p_weights * p) # consensus
            p = snowflake(*slush(p, p_weights, s, q_rate), c)

    return m

def population(p_size: int) -> array:
    """
    Returns a *uniformly* sampled population for given `p_size`
    where a value of `0` represents *yellow* and a value of `1`
    *red* cards.
    """
    return prg.integers(0, 2, size=p_size)

def counters(p_size: int) -> array:
    """
    Returns a zero-initialized array of conviction counters for
    the given population size (of `p_size`).
    """
    return zeros(p_size, dtype=numpy.int64)

def errors(ws: array, e_share=0.0) -> array:
    """
    Returns a stake-weighted population of adverserial members,
    with `e_share` being the *percentage* of the total weights.
    """
    return ws.cumsum() < e_share

def slush(
    p: array, ws: array, size: int, q_rate: float) -> array:
    """
    Applies the stake-weighted Slush polling mechanism for `p`:
    Make a random choice of a sample `size` (from a given array
    `p`) for *each* element within the array `p`. Then for each
    sample determine, if the α-majority of the sample indicates
    *red* (i.e. `1`) or *yellow* (i.e. `0`) cards.  However, if
    there is *no* α-majority (i.e. tie) within the sample, then
    do nothing.
    """
    ps = prg.choice(p, size=(size, p.size), p=ws).sum(axis=0)
    eq, gt = ps == (1-q_rate) * size, ps > (1-q_rate) * size

    return p * eq + gt, p, gt

def snowflake(
    n: array, p: array, gt: array, c: array) -> array:
    """
    Applies the Snowflake conviction model onto the population.
    """
    lt, gte = c < args.beta_1, c >= args.beta_1
    c += lt * (n == p) + gte * 0 ## color' == color => c[i]+= 1
    c *= lt * (n == p) + gte * 1 ## color' != color => c[i] = 0
    c += lt * (n != p) + gte * 0 ## color' != color => c[i] = 1
    c *= lt * (gt > 0) + gte * 1 ## *no* α-majority => c[i] = 0

    if args.debug_level > 0:
        print(p, file=sys.stderr)
    if args.debug_level > 1:
        print(n, file=sys.stderr)
    if args.debug_level > 2:
        print(c, file=sys.stderr)

    return (c < args.beta_1) * n + (c >= args.beta_1) * p

def weights(
    p_size: int, distribution: str, exponent: float) -> array:
    """
    Returns various weight distributions (ie validator stakes).
    """
    def norm(ws):
        ws_exp = numpy.power(ws, exponent)
        return numpy.sort(ws_exp) / ws_exp.sum()
    if distribution == 'cauchy':
        return norm(abs(prg.standard_cauchy(p_size)))
    elif distribution == 'equal':
        return norm(numpy.ones(p_size))
    elif distribution == 'exponential':
        return norm(prg.standard_exponential(p_size))
    elif distribution == 'gamma':
        _, shape = distribution.split('-')
        return norm(prg.standard_gamma(float(shape), p_size))
    elif distribution == 'normal':
        return norm(abs(prg.standard_normal(p_size)))
    elif distribution.startswith('pareto'):
        _, alpha = distribution.split('-')
        return norm(prg.pareto(float(alpha), p_size))
    elif distribution == 'total-weights':
        return norm(load(sys.stdin)[1])
    elif distribution == 'weights':
        return norm(load(sys.stdin)[0])
    else:
        return norm(prg.uniform(0, 1.0, p_size))

def load(file: TextIO) -> Tuple[array, array]:
    """
    Validator weights & total weights (i.e. w/[o] delegations).
    """
    ws = [] ## validator weight excl. delegations
    ts = [] ## validator weight incl. delegations

    for line in file.readlines():

        validators = json.loads(line)
        validators = validators['data']
        validators = validators['validators']
        validators = validators['results']

        ws.extend(map(lambda v: v['weight'], validators))
        ts.extend(map(lambda v: v['totalWeight'], validators))

    return array(ws), array(ts)

#######################################################################
#######################################################################

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='Produces the Avalanche simulation matrix '
                    '[max_round x max_sample]')
    parser.add_argument('-p', '--population',
        type=int, help='population size'
        ' (default: %(default)s)', default=10000)
    parser.add_argument('-d', '--distribution', choices=[
        'cauchy', 'equal', 'exponential', 'normal', 'uniform',
        'pareto-3', 'pareto-2', 'pareto-1', 'pareto-0.5',
        'gamma-3', 'gamma-2', 'gamma-1', 'gamma-0.5',
        'total-weights', 'weights'], ## i.e. stdin
        type=str, help='stake distribution'
        ' (default: %(default)s)', default='uniform')
    parser.add_argument('-x', '--distribution-exponent',
        type=float, help='stake distribution exponent'
        ' (default: %(default)s)', default=1.0)
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
        type=float, help='quorum rate in [0.0, 1.0]'
        ' (default: %(default)s)', default=0.70)
    parser.add_argument('-b1', '--beta-1',
        type=int, help='virtuous commit threshold '
        ' (default: %(default)s)', default=15)
    parser.add_argument('-e', '--error-share',
        type=float, help='error share in [0.0, 0.5]'
        ' (default: %(default)s)', default=0.00)
    parser.add_argument('--random-seed',
        type=int, help='random generator seed'
        ' (default: %(default)s)', default=None)
    parser.add_argument('--debug-level',
        type=int, choices=[0,1,2,3], help='debug level'
        ' (default: %(default)s)', default=0)

    args = parser.parse_args()
    prg = default_rng(args.random_seed)

    ws = weights(
        args.population,
        args.distribution,
        args.distribution_exponent)
    m = avalanche(
        ws, args.max_round,
        args.max_sample, args.min_sample,
        args.quorum_rate, args.error_share)

    args = vars(args)
    args['population'] = ws.size
    numpy.savetxt(sys.stdout, m, header=json.dumps(args))

#######################################################################
#######################################################################
