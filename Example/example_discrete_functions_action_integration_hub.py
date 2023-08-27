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
                                  times = 10,
                                  max_iterations = 30)

"""### An example with noise:"""

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

"""Notice that when I plot the second way the curves are smoothed."""