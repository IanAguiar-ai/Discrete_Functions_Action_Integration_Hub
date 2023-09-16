# -*- coding: utf-8 -*-
"""Example_Discrete_Functions_Action_Integration_Hub.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1vR5JQD7xSdInIqCYYoY4WZrrwmo6Opjg

## How to download:
"""

! pip install git+https://github.com/IanAguiar-ai/Discrete_Functions_Action_Integration_Hub

"""## Importing library:"""

from discrete_function import discrete_function

"""# Functionalities:

## Creating a discrete function:

$poisson(X = x) = \frac{\lambda^x * e^{-\lambda}}{x!}$
"""

def poisson(x:int, lambda_:float):
  def fatorial(n_):
    n = 1
    for i in range(2, n_ + 1):
      n *= i
    return n

  return (lambda_**x * 2.718281 ** (-lambda_))/fatorial(x)

"""## Passing the function to the class:"""

model = discrete_function(poisson, lambda_ = 3)

print(model)

"""## Getting function values:"""

print(model[0:10])

"""Note that the values were obtained where x goes from 0 to 10 including 10.

## Getting the accumulated values:
"""

print(model.accumulated(0, 10))

"""## Randomly taking samples according to this probability function."""

print(model.random(20))

"""Conditional Probability:"""

print(model[1:2] | model[1:4])

print(model[2,4,6] | model[0:6])

"""## Fitting curve parameter according to data:"""

sample = [poisson(i, lambda_ = 3.48261) for i in range(10)]
parameter = model.adjust_to_curve(name_param ='lambda_',
                                  curve = sample,
                                  initial_value = 1,
                                  plot = True,
                                  times = 1)

print(parameter)

"""### Example with more than one parameter:"""

def double_poisson(x:int, lambda_1:float, lambda_2:float, p):
  return poisson(x, lambda_1) * p + poisson(x, lambda_2) * (1 - p)

from random import random, seed
seed(1)

model_2 = discrete_function(double_poisson, lambda_1 = 1, lambda_2 = 1, p = 0.5)

sample = [double_poisson(i, lambda_1 = 3.48261, lambda_2 = 10.8362, p = 0.6) for i in range(20)]
parameter = model_2.adjust_to_curve(name_param = ['lambda_1', 'lambda_2', 'p'],
                                  curve = sample,
                                  initial_value = 1,
                                  plot = True,
                                  times = 6,
                                  max_iterations = 30)

"""Note that by increasing the number of iterations and 'times', convergence and therefore accuracy will be greater.

### An example with noise:
"""

seed(1)

model_2 = discrete_function(double_poisson, lambda_1 = 1, lambda_2 = 1, p = 0.5)

sample = [double_poisson(i, lambda_1 = 3.48261, lambda_2 = 10.8362, p = 0.6) + random() * 0.05 - 0.025 for i in range(20)]
parameter = model_2.adjust_to_curve(name_param = ['lambda_1', 'lambda_2', 'p'],
                                  curve = sample,
                                  initial_value = 1,
                                  plot = True,
                                  times = 6,
                                  max_iterations = 20)

"""### You can still order the chart individually:

Way 1:
"""

model_2.plot()

model_2.plot([1,10])

"""Way 2:"""

model_2[:32].plot()

model_2[1:10].plot()

"""Notice that when I plot the second way the curves are smoothed.

## Testing which model best fits the data:

Functions:
"""

from math import gamma

def fat(n:int):
    try:
        return gamma(n + 1)
    except:
        return 0

def poisson(x:int, lambda_:float):
    return 2.71828182**(-lambda_) * (lambda_**x)/fat(x)

def normal(x:int, mi:float, sigma:float):
    try:
        return (2.7182**(-(1/2)*((x - mi)/sigma)**2)) / (sigma * (2*3.1415)**(1/2))
    except:
        return 0

"""models:"""

from discrete_function import adjust_sample_on

curve = [normal(i, mi = 6.74, sigma = 4.25) + random() * 0.04 - 0.02 for i in range(0, 15)]

model_1 = discrete_function(poisson, lambda_ = 1)
model_2 = discrete_function(normal, sigma = 1, mi = 1)
model_3 = discrete_function(double_poisson, lambda_1 = 1, lambda_2 = 1, p = 0.5)

best_model = adjust_sample_on(curve, [model_1, model_2, model_3],
                              plot = True)

"""Notice that he found the function that best fits the data:"""

print(best_model)
best_model[-6:20].plot()

"""### With a non-sequential x:"""

x = [0, 3, 5, 6, 7, 11, 15]

curve = [normal(i, mi = 6.74, sigma = 4.25) + random() * 0.01 - 0.005 for i in x]

model_1 = discrete_function(poisson, lambda_ = 1)
model_2 = discrete_function(normal, sigma = 1, mi = 1)
model_3 = discrete_function(double_poisson, lambda_1 = 1, lambda_2 = 1, p = 0.5)

best_model = adjust_sample_on(curve = curve,
                              models = [model_1, model_2, model_3],
                              x = x,
                              plot = True)

"""### Example with sine:"""

from math import sin, cos

def s2(x, a, b):
    return sin(x*a) + sin(x*b)

def c2(x, a, b):
    return cos(x*a) + cos(x*b)

model_1 = discrete_function(s2, a = 1, b = 1)
model_2 = discrete_function(c2, a = 1, b = 1)

x = [i * 0.1 for i in range(10)]
curve = [s2(i, a = 3, b = 7) for i in x]

best_model = adjust_sample_on(curve = curve, x = x,
                              models = [model_1, model_2],
                              times = 10,
                              initial_value = 0.1,
                              plot = True)

"""## Function mixes:"""

def s(x, sa, **rest): #sin
    return sin(x*sa)

def c(x, ca, **rest): #cos
    return cos(x*ca)

"""### Mixing:"""

model_1 = discrete_function(s, sa = 1)
model_2 = discrete_function(c, ca = 1)

final_model = model_1 + model_2

x = [i * 0.1 for i in range(10)]
curve = [s(i, sa = 3) + c(i, ca = 4) for i in x]

best_model = adjust_sample_on(curve = curve, x = x,
                              models = [final_model],
                              times = 20,
                              initial_value = 0.1,
                              plot = True)

"""### Complex mixtures:"""

def linear(x, la, lb, **rest):
  return la + x*lb

model_1 = discrete_function(s, sa = 1)
model_2 = discrete_function(c, ca = 1)
model_3 = discrete_function(linear, la = 1, lb = 1)

final_model = (model_1 + model_2 - 1) * (model_3/3)

x = [i * 0.1 for i in range(10)]
curve = [(s(i, sa = 3) + c(i, ca = 20) - 1) * (linear(i, la = 12, lb = 40)/3) for i in x]

best_model = adjust_sample_on(curve = curve, x = x,
                              models = [final_model],
                              times = 15,
                              initial_value = 0.1,
                              plot = True)