# Consensus by Avalanche

— by **Hasan Karahan** [#Blockchain], [#Avalanche], [#AVA]

[#Blockchain]: https://twitter.com/search?q=%23blockchain
[#Avalanche]: https://twitter.com/search?q=%23avalanche
[#AVA]: https://twitter.com/search?q=%23ava

## Introduction

Let's assume you are watching a soccer game in a very large stadium built for such an event. Further, let's assume that the capacity of the stadium is about one hundred thousand people. So the *population* $\mathcal{P}$ has a size of:

$$\begin{equation}
|\mathcal{P}| = 100'000\tag{$\star$}
\end{equation}$$

Now, let's give the game a twist and ascribe to the spectators a dislike for centralized decision making: They'll reflect such distaste equally in the soccer game and prefer to *not* have a referee. Or rather, they have restricted the power of the referee to *not* being able to issue a *yellow* or a *red* card upon a foul.

So, what happens when there is a situation where a player engages another player unfairly, but where it is not so clear if the situation deserves a *yellow* or a *red* punishment? The referee cannot issue a decision because otherwise the spectators would rip him apart for transgressing his powers.

So, they themselves have to decide: But the decision should be made *almost* unanimously, otherwise it does not count. To enable all of the $100'000$ people to converge quickly to the same conclusion, everybody agrees to the following *consensus* rules:

1. Upon an unfair behavior make an *individual* decision if the culprit deserves a *yellow* or a *red* punishment and then raise your card, such that it is easily visible for everybody else.

2. Then take a *random sample* of $n$ people among the other fellow spectators in the stadium and change your *own* card according to the *majority* of those people you have chosen; but stick to your card if there is a tie.

3. Iterate the second step until the *whole* (or almost whole) stadium displays the same color.

## Formalism

For each person $p$ among all the population $\mathcal{P}$ and a given round $r\in\mathbb{N}$ we can define a ${card}_r(p)$ as:

$$\begin{equation}
{card}_{r}(p) =\begin{cases}
1_{red}
& |\mathbb{S}_{1_{red}}^{(r)}(p)| > {n}\big{/}{2},\\
{card}_{r-1}(p)
& |\mathbb{S}_{1_{red}}^{(r)}(p)| = {n}\big{/}{2},\\
0_{yellow}
& otherwise;
\end{cases}
\end{equation}$$

where we encode a value of $1$ for $red$ and $0$ for $yellow$ cards, and where the *sample set* $\mathbb{S}_{color}$ is defined as:

$$\begin{equation}
\mathbb{S}_{color}^{(r)}(p) = \big\{
  s \mid {s\in{sample_{r}(p)}}\land{s=color}
\big\}
\end{equation}$$

where $sample_r(p)$ is defined as:

$$\begin{equation}sample_r(p) = \big\{
   {card_{r-1}(p_i) \mid p_i\hat\in{\mathcal{P}}}
   \land
   {i\in{\{1..n\}}}
\big\}\end{equation}$$

where each $p_i\hat\in{\mathcal{P}}$ denotes a random selection of $p_i$ from the population $\mathcal{P}$ according to the *uniform* distribution, i.e. probability $\mathbb{P}(p_i) = 1\big/|\mathcal{P}|$ for each $p_i\in{\mathcal{P}}$.

**Summarized:** People keep influencing each other, until everybody hopefully converges onto the same opinion.

## Simulation

There is now a very interesting question that needs to be clarified:

> How *many* rounds does it usually take to reach consensus, i.e. until almost the whole stadium displays either $red$ or $yellow$ cards?

We have answered this question by running multiple simulations of the whole process as described above, and found that the number of rounds required to reach consensus is dependent on:

* the total population $|\mathcal{P}|$, where the larger it gets the *more* rounds need to be iterated, and also on

* the number of people randomly sampled in each round i.e. $|\mathbb{S}_{color}^{(r)}(p)|$, where for larger sample sizes *fewer* rounds need to be iterated.

The simulation is using the term *avalanche*, since the change of opinions is reminiscent of an avalanche, where the *higher* the percentage of people (in a given round $r$) thinking for example that a foul should be punished with *red*, the *higher* the probability of people changing their opinion from *yellow* to *red* (in the next round $r+1$).

### Aggregate over $1'000$ simulations for $|\mathcal{P}|=100'000$:

<figure style="margin: 1em 0;"><iframe style="border: none; max-width: 100%;" src="https://drive.google.com/file/d/1IzMsjkpXRCHbmVeZZ9_xT5Qu29f4kWbh/preview" width=600 height=222></iframe><figcaption>$|\mathcal{P}|=10^5$: Consensus for <em>sample sizes</em> $|\mathbb{S}|\in{[2..10]}$ and $rounds\in{[1..13]}$</figcaption></figure>

For a population of $100'000$ people consensus can be achieved within $13$ rounds, where it is reached faster when more fellow spectators are taken into consideration: A sample size of $|\mathbb{S}|=8$ (or more) seems to produce average and median consensus levels very close to $100\%$ with a tiny standard deviation, while having reasonably low amounts of outliers.

<figure style="margin: 1em 0;"><iframe style="border: none; max-width: 100%;" src="https://drive.google.com/file/d/1l3y75wxU2E_v3OEpryFoSyD0en4qkJFp/preview" width=600 height=222></iframe><figcaption>$|\mathcal{P}|=10^5$: Consensus for <em>sample sizes</em> $|\mathbb{S}|\in{[2..10]}$ and $rounds\in{[1..13]}$</figcaption></figure>

The same simulation data shown here as histograms yields overall the same results as above with the box plots.

### Aggregate over $1'000$ simulations for $|\mathcal{P}|=1'000'000$:

<figure style="margin: 1em 0;"><iframe style="border: none; max-width: 100%;" src="https://drive.google.com/file/d/1M1O78woKD61-uzz_1JbR4nY65wHPZXN5/preview" width=600 height=222></iframe><figcaption>$|\mathcal{P}|=10^6$: Consensus for <em>sample sizes</em> $|\mathbb{S}|\in{[2..10]}$ and $rounds\in{[1..13]}$</figcaption></figure>

One may expect, that by drastically increasing the population size  by an order to $|\mathcal{P}|=1'000'000$ people, a similar increase of the sample size and rounds would be required, however that does not seem to be the case: While there is a small decrease in consensus, it is almost not perceptible (for the same sample size of $8$ and same number of rounds of $13$). However, the number of outliers seems to increase while still being reasonable.

<figure style="margin: 1em 0;"><iframe style="border: none; max-width: 100%;" src="https://drive.google.com/file/d/1HEreI5THkv20C3955v0LVEY60sAZpssQ/preview" width=600 height=222></iframe><figcaption>$|\mathcal{P}|=10^6$: Consensus for <em>sample sizes</em> $|\mathbb{S}|\in{[2..10]}$ and $rounds\in{[1..13]}$</figcaption></figure>

Again, using histograms for the visualization of the same simulations for a population of one million leads to the same conclusions as above with the box plots.

## Conclusion

The overall approach of using the model of an *avalanche* seems to be an efficient process of generating consensus among a very large population. While there seems to be an *engineering trade-off* between a lower sample size and a higher number of rounds, sampling $8$ or more fellow spectators over $13$ rounds seems to be a good choice, given a population of $100'000$ people. Also, these parameters can be applied to a much larger crowd of *one million* people without almost any significant decrease in consensus.

## Appendix

### The `avalache.py` simulator

Simulates for the provided *population size* $|\mathcal{P}|$, maximum *sample size* $|\mathbb{S}|$ and maximum number of *rounds* the *avalanche* process:

```python
#!/usr/bin/env python
```
```python
from typing import Dict

from numpy.random import choice
from numpy.random import randint

from numpy import array
from numpy import maximum
from numpy import round
from numpy import zeros

from matplotlib import pyplot as pp

import argparse
import json
import numpy
import sys
```
```python
def avalanche(
    population_size: int, max_sample: int, max_round: int
) -> array:
```
```python
    """
    Simulates for the provided number of `max_round`, the given
    `population_size` and `max_sample` the *avalanche* process,
    where we keep the `population_size` fixed, but consider all
    sample sizes from `1` until `max_sample` (inclusive);  then
    return a matrix (array) `m` for each round and sample size.

    While technically it is not required to use the matrix `m`,
    and rely *only* on the array `p`  (to successfully simulate
    the avalanche process), it is used for book-keeping helping
    later-on to generate plots of the entire process.
    """
```
```python
    m = zeros(shape=(max_round, max_sample))
    for s in range(max_sample):

        p = population(size=population_size)
        for r in range(max_round):

            m[r, s] = p.sum() / population_size
            p = resample(p, s + 1)

    return m
```
```python
def population(size: int) -> array:
```
```python
    """
    Returns a uniformly sampled population for the given `size`
    where a value of `0` represents *yellow* and a value of `1`
    *red* cards.
    """
```
```python
    return randint(0, 2, size=size)
```
```python
def resample(p: array, size: int) -> array:
```
```python
    """
    Make a random choice of a sample `size` (from a given array
    `p`) for *each* element within the array `p`. Then for each
    sample calculate, if the majority of the sample indicates a
    *red* (i.e. `1`) or a *yellow* (i.e. `0`) card. However, if
    there is *no* majority (i.e. a tie) within the sample, then
    do nothing.

    Note that the returned array has the same size as the array
    `p`: It represents a state update of `p`, where elements of
    the array have switched their "opinion" with respect to the
    majority they have sampled.
    """
```
```python
    ps = choice(p, size=(size, p.size)).sum(axis=0)
    eq, gt = ps == size / 2.0, ps > size / 2.0

    return p * eq + gt
```
```python
if __name__ == '__main__':
```
```python
    parser = argparse.ArgumentParser(
        description='Produces the Avalanche Matrix '
                    '[rounds x max.sample-size]')

    parser.add_argument('-p', '--population',
        type=int, help='population size '
        '(default: %(default)s)', default=100000)
    parser.add_argument('-r', '--max-round',
        type=int, help='maximum number of rounds '
        '(default: %(default)s)', default=13)
    parser.add_argument('-s', '--max-sample',
        type=int, help='maximum sample size '
        '(default: %(default)s)', default=10)

    args = parser.parse_args()

    m = avalanche(
        args.population, args.max_sample, args.max_round)
    numpy.savetxt(
        sys.stdout, m, header=json.dumps(vars(args)))
```

Running a *single* simulation for the population size of $|\mathcal{P}|=100'000$ people yields the matrix below, where the *rows* display the rounds in the range of $[1..13]$ and the *columns* iterate over the sample sizes of $[1..10]$:

```bash
$ ./avalanche.py --population=100000 --max-sample=10 --max-round=13
```
```bash
# {"population": 100000, "max_sample": 10, "max_round": 13}
4.988699999999999801e-01 4.966800000000000104e-01 4.984000000000000097e-01 5.022699999999999942e-01 5.014100000000000223e-01 5.012299999999999534e-01 5.022900000000000142e-01 5.009400000000000519e-01 5.020000000000000018e-01 5.022199999999999998e-01
4.988299999999999956e-01 4.967199999999999949e-01 4.961999999999999744e-01 5.048200000000000465e-01 5.040599999999999525e-01 5.027399999999999647e-01 5.079200000000000381e-01 5.044100000000000250e-01 5.049900000000000500e-01 5.068599999999999772e-01
5.008399999999999519e-01 4.946300000000000141e-01 4.975700000000000123e-01 5.091999999999999860e-01 5.078399999999999581e-01 5.056699999999999529e-01 5.165199999999999791e-01 5.125600000000000156e-01 5.125399999999999956e-01 5.180099999999999705e-01
5.001700000000000035e-01 4.928899999999999948e-01 4.971099999999999963e-01 5.179200000000000470e-01 5.152900000000000258e-01 5.101200000000000179e-01 5.370099999999999874e-01 5.320200000000000484e-01 5.312400000000000455e-01 5.497100000000000319e-01
4.999100000000000210e-01 4.890999999999999792e-01 4.946800000000000086e-01 5.317199999999999704e-01 5.306300000000000461e-01 5.204100000000000392e-01 5.826999999999999957e-01 5.774500000000000188e-01 5.754700000000000371e-01 6.302799999999999514e-01
5.019000000000000128e-01 4.824499999999999900e-01 4.934000000000000052e-01 5.604200000000000292e-01 5.594000000000000083e-01 5.454499999999999904e-01 6.734200000000000186e-01 6.862800000000000011e-01 6.799100000000000144e-01 8.149999999999999467e-01
5.020700000000000163e-01 4.750900000000000123e-01 4.914999999999999925e-01 6.127299999999999969e-01 6.083399999999999919e-01 5.992399999999999949e-01 8.385000000000000231e-01 8.855800000000000338e-01 8.746000000000000441e-01 9.923300000000000454e-01
4.981400000000000272e-01 4.623099999999999987e-01 4.866599999999999815e-01 7.039199999999999902e-01 6.959999999999999520e-01 7.061199999999999699e-01 9.845000000000000417e-01 9.983600000000000252e-01 9.976399999999999713e-01 1.000000000000000000e+00
5.013100000000000334e-01 4.423199999999999910e-01 4.833500000000000019e-01 8.430499999999999661e-01 8.304599999999999760e-01 8.831599999999999451e-01 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00
5.021499999999999853e-01 4.149599999999999955e-01 4.769399999999999751e-01 9.706099999999999728e-01 9.632399999999999851e-01 9.950499999999999901e-01 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00
5.045800000000000285e-01 3.738000000000000211e-01 4.657899999999999818e-01 9.998099999999999765e-01 9.995000000000000551e-01 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00
5.050700000000000189e-01 3.149700000000000277e-01 4.497700000000000031e-01 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00
5.029900000000000482e-01 2.368300000000000127e-01 4.264899999999999802e-01 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00 1.000000000000000000e+00
```

<!-- ------------------------------------------------------------------
  -- CSS Styles: body
  -- ----------------------------------------------------------------->

<style>
  body {
    margin: 0 auto;
    max-width: 768px;
    padding: 0.5em;
  }
  body {
    columns: auto 1;
  }
</style>

<!-- ------------------------------------------------------------------
  -- CSS Styles: headers
  -- ----------------------------------------------------------------->

<style>
  h1 {
    column-span: all;
    text-align: center;
  }
  h1, h2, h3, h4, h5, h6 {
    margin: 0.5em 0;
  }
</style>

<style>
  body {
    counter-reset: h1-headings;
  }
  h1 {
    counter-increment: h1-headings;
    counter-reset: h2-headings;
  }
  h1:before {
    content: "";
  }
  h2 {
    counter-increment: h2-headings;
    counter-reset: h3-headings;
  }
  h2:before {
    content: counter(h2-headings) " ";
  }
  h3 {
    counter-increment: h3-headings;
  }
  h3:before {
    content: counter(h2-headings) "."
             counter(h3-headings) " ";
  }
</style>

<!-- ------------------------------------------------------------------
  -- CSS Styles: paragraphs
  -- ----------------------------------------------------------------->

<style>
  p {
    margin: 0.5em 0;
  }
  p, li, figcaption {
    text-align: justify;
  }
</style>

<!-- ------------------------------------------------------------------
  -- CSS Styles: figures
  -- ----------------------------------------------------------------->

<style>
  figure {
    margin: 1em;
    width: 100%;
    text-align: center;
  }
  figure>img {
    border: none;
    border-radius: 1mm;
  }
  figure>img {
    width: 100%;
  }
  figure>iframe {
      border-radius: 3px;
  }
  figure>figcaption {
    font-size: smaller;
    margin-top: 1em;
    text-align: center;
    width: 100%;
  }
</style>

<style>
  body {
    counter-reset: figures;
  }
  figure>figcaption {
    counter-increment: figures;
  }
  figure>figcaption:before {
    content: 'Fig. ' counter(figures) ' – ';
  }
</style>

<!-- ------------------------------------------------------------------
  -- CSS Styles: code blocks
  -- ----------------------------------------------------------------->

<style>
  @import url(
      'https:////cdn.jsdelivr.net/gh/highlightjs/cdn-release@10/build/styles/default.min.css'
  );
</style>

<style>
  pre {
    border: none;
    border-radius: 1mm;
  }
  pre {
    background-color: #f5f5f5;
    margin: 1em;
    overflow-x: auto;
    padding: 1em;
    white-space: nowrap;
    width: calc(100% - 4em);
  }
  pre>code {
    white-space: pre;
  }
</style>

<!-- ------------------------------------------------------------------
  -- CSS Styles: blockquotes
  -- ----------------------------------------------------------------->

<style>
  blockquote {
    margin: 1em;
    padding: 0.5em 1em;
    width: calc(100% - 2em);
  }
</style>


<!-- ------------------------------------------------------------------
  -- JS Script: MathJax
  -- ----------------------------------------------------------------->

<script>
  function script(url) {
    const element = document.createElement('script');
    element.src = url; element.async = true;
    document.head.appendChild(element);
  };
  window.MathJax = {
    options: {
      renderActions: {
        addMenu: [], checkLoading: []
      }
    },
    startup: {
      ready: () => {
        MathJax.startup.defaultReady();
      }
    },
    tex: {
      inlineMath: [['$', '$'], ['$$', '$$']],
      tags: 'ams',
    },
    svg: {
      fontCache: 'global'
    },
  };
  script(
    'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js'
  );
</script>

<!-- ############################################################## -->
