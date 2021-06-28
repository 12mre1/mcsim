# mcsim
A python package for Monte Carlo simulation methods.

## Installation

`pysim` is available from the `pypi` repository, and you can install it directly from the command line:
```{console}
pip install mcsim
```
Or for some operating systems:
```{console}
python3 -m pip install mcsim
```
If you'd like to test it in a virtual environment without altering your main python installation,
assuming you have `venv` installed:
```{python}
python3 -m venv <env_name>
source env_name/bin/activate
pip install mcsim
```
Then just delete the environment when you're done.

## Examples
The `MCIntegrator` class, along with the pdf functions can be used to compute standard probabilities or moments:
```{python}
import mcsim
from mcsim.pdfs import pdf_normal

# Instantiate the object (no args required yet)
integral = MCIntegrator()

# Fit a specific integral (standard normal density from 0 to 1)
integral.fit(lwr = 0, upr = 1, func = pdf_normal)

# Access useful properties
print('Standard Error: {}'.format(integral.se_hat))
print('Integral Value: {}'.format(integral.ihat))
print('Confidence Interval: {}'.format(integral.get_confidence_intervals(alpha=0.05)))
```
```{console}
Standard Error: 5.55389276409176e-18
Integral Value: 0.343389156010687
Confidence Interval: (0.343389156010687, 0.343389156010687)
```
But the function needn't be a statistical density. You can compute any definite integral. Note that the larger is N 
(number of samples) the more precise will be the estimate.

- The `ImportanceSampler` class is very useful for computing moments of distributions that are difficult to sample.
- E.g suppose you cannot easily sample the exponential(2) distribution, but want to find its second moment (x^2)
- We know the result should be: Var(x) + (E(x))^2 = (1/2^2) + (1/2)^2 = 0.5.
```{python}
from mcsim.pdfs import pdf_exponential
import scipy.stats
import numpy as np

# Instantiate importance sampler (note the tails)
sampler = ImportanceSampler(tails=1, N=100000)
print(sampler)

# Specify moment as function
exp_function = lambda x: x**2

# Fit the sampler
sampler.fit(f = pdf_exponential, h = exp_function)
print(sampler.ihat)
print(sampler.se_hat)
```
```{console}
MC Sample size: 100000, Number of tails: 1
0.5014337356281615
3.6166806084671604e-17
```
We get a very close approximation.


## Details

`mcsim` contains several objects designed to perform Monte Carlo simulation methods. 

Current objects include:
- `MCIntegrator()`: Computes a numerical integral given a user-specified function, and integration bounds.
   - You can extract the integral itself, as well as the standard error, and the confidence interval for
   a given level of significance.
- `ImportanceSampler()`: Computes expectations in cases where the integrating density cannot easily be
   sampled. This often arises in Bayesian posterior computations. See the technical section for more
   detail. Note that you must specify the number of tails when instantiating the object (`tails=2` is
   the default). Returns the same information as the `MCIntegrator` class.

As with some transformers in `scikit-learn`, you do not have to instantiate an `mcsim` object 
with any hyperparameters. However you do need to specify these when calling the `.fit()` method.
Until the `.fit()` method is called, most useful attributes will not be available (for example, the 
`MCIntegrator()` class only computes the integral and standard error attributes when the fit method
is called). Confidence intervals are computed with a separate method (`.get_confidence_interval()`) 
which can only be called after `.fit()`.

In addition to the MC objects, the `pdfs.py` file contains many useful statistical density functions
you can pass as arguments. These functions are necessarily continuous (not discrete). They are all
prefixed with `pdf_` (for example `pdf_normal`):
- Normal (`pdf_normal`)
- Exponential (`pdf_exponential`)
- Uniform (`pdf_uniform`)
- Student-T (`pdf_studentt`)
- Rayleigh (`pdf_rayleigh`)
- Weibull (`pdf_weibull`)
- Chi-square (`pdf_chisquare`)
- Beta (`pdf_beta`)
- Gamma (`pdf_gamma`)
- Fisher (F) (`pdf_fisher`)
- Laplace (`pdf_laplace`)
- Pareto (`pdf_pareto`)

## Testing

## Technical 

- The `MCIntegrator` class approximates integration based on the fact that definite integrals can be rewritten:

<center>
<a href="https://www.codecogs.com/eqnedit.php?latex=I&space;=&space;\int_{a}^{b}&space;h(x)&space;dx&space;=&space;\int_{a}^{b}&space;h(x)(b&space;-&space;a)&space;\cdot&space;\frac{1}{b-a}dx&space;=&space;\int_{a}^{b}&space;w(x)&space;f(x)dx&space;=&space;E_{U(a,b)}(w(x))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?I&space;=&space;\int_{a}^{b}&space;h(x)&space;dx&space;=&space;\int_{a}^{b}&space;h(x)(b&space;-&space;a)&space;\cdot&space;\frac{1}{b-a}dx&space;=&space;\int_{a}^{b}&space;w(x)&space;f(x)dx&space;=&space;E_{U(a,b)}(w(x))" title="I = \int_{a}^{b} h(x) dx = \int_{a}^{b} h(x)(b - a) \cdot \frac{1}{b-a}dx = \int_{a}^{b} w(x) f(x)dx = E_{U(a,b)}(w(x))" /></a>
</center>

So computing any integral just involves the application of the Law of Large Numbers:

<a href="https://www.codecogs.com/eqnedit.php?latex=\hat{I}&space;=&space;\frac{1}{N}&space;\sum_{i=1}^{N}&space;w(X_i)&space;\rightarrow_{p}&space;E(w(X))" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\hat{I}&space;=&space;\frac{1}{N}&space;\sum_{i=1}^{N}&space;w(X_i)&space;\rightarrow_{p}&space;E(w(X))" title="\hat{I} = \frac{1}{N} \sum_{i=1}^{N} w(X_i) \rightarrow_{p} E(w(X))" /></a>

The `ImportanceSampler` class considers the case where we cannot easily sample from f(x). In this case we again rewrite the expression:

<a href="https://www.codecogs.com/eqnedit.php?latex=I&space;=&space;\int&space;h(x)&space;f(x)&space;dx&space;=&space;\int&space;\frac{h(x)f(x)}{g(x)}&space;g(x)dx&space;=&space;E_g(Y)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?I&space;=&space;\int&space;h(x)&space;f(x)&space;dx&space;=&space;\int&space;\frac{h(x)f(x)}{g(x)}&space;g(x)dx&space;=&space;E_g(Y)" title="I = \int h(x) f(x) dx = \int \frac{h(x)f(x)}{g(x)} g(x)dx = E_g(Y)" /></a>

Thus we can compute the expectation over a different distribution we can more easily sample from. This is common in posterior inference under Bayesian sampling scenarios.
One pitfall is that the redefined expectation may have infinite standard error, if g(x) has thinner tails than f(x). To try and avoid this, the standard g(x) functions
I use have very heavy tails: Cauchy distribution for two-tailed and Pareto distribution for one-tailed. As with MC Integration, the sample estimate converges to the true
expectation by Law of Large Numbers.

## Future Work

- The `MCIntegrator` is currently based on sampling from a Uniform Density. There is a more general version I'm 
planning to implement. The uniform version will likely become a subclass of this.

- I'm planning on implementing some variations of Markov-Chain Monte-Carlo Estimation. They will have a similar layout
 to the `MCIntegrator` and `ImportanceSampler`. For example:
    - Metropolis-Hastings 
    - Gibbs Sampling
    - Random-walk Metropolis Hastings
    
- The `ImportanceSampler` class would ideally define the scaling distribution based on f(x). However, since f(x) is definitionally hard to sample, 
  it is not obvious how to do this. Solving this problem would fix the possibility of infinite standard error.
