[![Build Status](https://travis-ci.com/hsk81/avalanche-sim.svg?branch=master)](https://travis-ci.com/hsk81/avalanche-sim)

# Avalanche Sim

An advanced simulator for the [Avalanche] consensus algorithm: It supports the simulation of *millions* of nodes, and has a built-in error model to mimic malicious participants trying to sabotage the network:

![Boxplot for 10k Nodes and Error Share of 15%](./data/visualization/boxplot/1K@P1E6.R01:20.S20:20.Q70.E15.svg)

Above, you see the [Avalanche] consensus in action using the same parameters as the actual `mainnet`, i.e. the number of *rounds* is `20`, the size of *subsamples* is also `20` and the *quorum* rate is `70%` of the subsample size (i.e. `14`).

In addition, `15%` of the network participants (by stake) are modeled to be malicious, which actively try to sabotage the network *in each round* from reaching the maximum possible consensus level (which in this example happens to be `85%`, because `15%` of the network is malicious). Let's have a closer look by zooming in:

![Boxplot for 10k Nodes and Error Share of 15%](./data/visualization/boxplot/1K@P1E6.R03:20.S20:20.Q70.E15.svg)

The graphs have been produced by running `1'000` simulations over `10'000` nodes, and it is clearly observeable that the network easily and *very quickly* reaches the maximum possible consensus level, and then tightly *maintains* it &ndash; despite *constant* interference by malicious network participants!

## Prerequisite(s)

```
Name        : python
Version     : 3
Description : Next generation of the python high-level scripting language
URL         : https://www.python.org/
```

## Installation

```sh
$ ./setup.sh ## setup virtual Python environment
```
```sh
$ source bin/activate ## activate virtual Python environment
```
```sh
[avalanche] $ ./setup.py install ## setup Python dependencies
```
```sh
[avalanche] $ cd ./source ## change directory to ./source
```

## Simulator

```sh
[avalanche] $ ./avalanche.py --help
```
```
usage: avalanche.py [-h] [-p POPULATION]
  [-d {cauchy,uniform,equal,pareto-1,...}]
  [-R MAX_ROUND] [-s MIN_SAMPLE] [-S MAX_SAMPLE]
  [-q QUORUM_RATE] [-e ERROR_SHARE]
  [--random-seed RANDOM_SEED]

Produces the Avalanche simulation matrix [max_round x max_sample]

optional arguments:
  -h, --help            show this help message and exit
  -p POPULATION, --population POPULATION
                        population size (default: 10000)
  -d {...}, --distribution {cauchy,uniform,equal,pareto-1,...}
                        stake distribution (default: uniform)
  -R MAX_ROUND, --max-round MAX_ROUND
                        maximum number of rounds (default: 20)
  -s MIN_SAMPLE, --min-sample MIN_SAMPLE
                        minimum sample size (default: 1)
  -S MAX_SAMPLE, --max-sample MAX_SAMPLE
                        maximum sample size (default: 20)
  -q QUORUM_RATE, --quorum-rate QUORUM_RATE
                        quorum rate (default: 0.7)
  -e ERROR_SHARE, --error-share ERROR_SHARE
                        error share in [0.0, 0.5) (default: 0.0)
  --random-seed RANDOM_SEED
                        random generator seed (default: None)
```

## Boxplot

```sh
[avalanche] $ ./boxplot.py --help
```
```
usage: boxplot.py [-h] [-r MIN_ROUND] [-R MAX_ROUND]
                       [-s MIN_SAMPLE] [-S MAX_SAMPLE]

Plots the Avalanche simulation matrix as boxplots

optional arguments:
  -h, --help            show this help message and exit
  -r MIN_ROUND, --min-round MIN_ROUND
                        minimum round (default: 0)
  -R MAX_ROUND, --max-round MAX_ROUND
                        maximum round (default: None)
  -s MIN_SAMPLE, --min-sample MIN_SAMPLE
                        minimum sample size (default: None)
  -S MAX_SAMPLE, --max-sample MAX_SAMPLE
                        maximum sample size (default: None)
```

## Histogram

```sh
$ ./histogram.py --help
```
```
usage: histogram.py [-h] [-b BINS] [-c COLOR_MAP]
                         [-r MIN_ROUND] [-R MAX_ROUND]
                         [-s MIN_SAMPLE] [-S MAX_SAMPLE]

Plots the Avalanche simulation matrix as historams

optional arguments:
  -h, --help            show this help message and exit
  -b BINS, --bins BINS  histogram bins (default: 5)
  -c COLOR_MAP, --color-map COLOR_MAP
                        color map (default: plasma)
  -r MIN_ROUND, --min-round MIN_ROUND
                        minimum round (default: 0)
  -R MAX_ROUND, --max-round MAX_ROUND
                        maximum round (default: None)
  -s MIN_SAMPLE, --min-sample MIN_SAMPLE
                        minimum sample size (default: None)
  -S MAX_SAMPLE, --max-sample MAX_SAMPLE
                        maximum sample size (default: None)
```

## Examples

### 1a) *Single* simulation run over 10'000 nodes & sample sizes in [1, 20]:

```sh
[avalanche] $ ./avalanche.py
```

```
# {"population": 10000, "distribution": "uniform", "max_round": 20, "min_sample": 1, "max_sample": 20, "quorum_rate": 0.7, "error_share": 0.0, "random_seed": null}
4.996999999999999775e-01 5.006000000000000449e-01 ... 5.038000000000000256e-01 5.023999999999999577e-01
5.069000000000000172e-01 2.523000000000000242e-01 ... 3.209999999999999659e-02 4.170000000000000095e-02
...
5.305999999999999606e-01 0.000000000000000000e+00 ... 0.000000000000000000e+00 0.000000000000000000e+00
5.330000000000000293e-01 0.000000000000000000e+00 ... 0.000000000000000000e+00 0.000000000000000000e+00
```

#### Plots:

```sh
[avalanche] $ ./avalanche.py | ./boxplot.py
```

```sh
[avalanche] $ ./avalanche.py | ./histogram.py
```

### 1b) *Single* simulation run over 10'000 nodes & sample size of 20:

```sh
[avalanche] $ ./avalanche.py --min-sample=20
```

```
# {"population": 10000, "distribution": "uniform", "max_round": 20, "min_sample": 20, "max_sample": 20, "quorum_rate": 0.7, "error_share": 0.0, "random_seed": null}
0.000000000000000000e+00 0.000000000000000000e+00 ... 0.000000000000000000e+00 5.011999999999999789e-01
0.000000000000000000e+00 0.000000000000000000e+00 ... 0.000000000000000000e+00 4.000000000000000083e-02
...
0.000000000000000000e+00 0.000000000000000000e+00 ... 0.000000000000000000e+00 0.000000000000000000e+00
0.000000000000000000e+00 0.000000000000000000e+00 ... 0.000000000000000000e+00 0.000000000000000000e+00
```

#### Plots:

```sh
[avalanche] $ ./avalanche.py -s20 | ./boxplot.py
```

```sh
[avalanche] $ ./avalanche.py -s20 | ./histogram.py
```

### 2a) 1'000 simulation runs over 10'000 nodes & sample sizes in [1, 20]:

```sh
[avalanche] $ time ./avalanche.sh 1000 > /tmp/P1E4.R01:20.S01:20.Q70.E00.txt
```
```sh
real    20m0.000s
user    20m0.000s
sys     20m0.000s
```

..where `avalanche.sh` is a wrapper around `avalanche.py` iterating over the latter by the provided *number of simulations*. Otherwise, it accepts the same arguments as the wrapped script.

#### Plots:

```sh
[avalanche] $ ./boxplot.py < /tmp/P1E4.R01:20.S01\:20.Q70.E00.txt
```

```sh
[avalanche] $ ./histogram.py < /tmp/P1E4.R01:20.S01\:20.Q70.E00.txt
```

### 2b) 1'000 simulation runs over 10'000 nodes & sample size of 20:

```sh
[avalanche] $ time ./avalanche.sh 1000 -s20 > /tmp/P1E4.R01:20.S20:20.Q70.E00.txt
```
```sh
real    1m0.000s
user    1m0.000s
sys     1m0.000s
```

..where `avalanche.sh` is a wrapper around `avalanche.py` iterating over the latter by the provided *number of simulations*. Otherwise, it accepts the same arguments as the wrapped script.

#### Plots:

```sh
[avalanche] $ ./boxplot.py < /tmp/P1E4.R01:20.S20\:20.Q70.E00.txt
```

```sh
[avalanche] $ ./histogram.py < /tmp/P1E4.R01:20.S20\:20.Q70.E00.txt
```

## Further information:

* https://calaganne.blogspot.com/2018/11/consensus-by-avalanche.html

## Copyright

 © 2021, [Hasan Karahan](mailto:avalanche@blackhan.com), MSc ETH Zurich.

[Avalanche]: https://www.avalabs.org/whitepapers
