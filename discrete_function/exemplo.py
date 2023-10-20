from discrete_function import Discrete_function, adjust_sample_on

def exp(x:float, a:float, k:float):
    return x*(a)**(1 + k)

def quadratica_inversa(x:float, a:float, b:float, k:float):
    return -a*(x - k)**2 + b*10

def quadratica(x:float, a:float, b:float, k:float):
    return a*(x - k)**2 + b

def simples(x:float, a:float, b:float, **resto):
    return a*x + b

def simples_dupla(x:float, a1:float, b1:float, a2:float, b2:float, limiar:float, **resto):
    if x < limiar * 10:
        return a1*x + b1
    else:
        return a2*x + b2

def simples_dupla_suave(x:float, a1:float, b1:float, a2:float, b2:float):
    return (a1*x + b1) *(x/300) + (a2*x + b2) * (1- x/300)

def simples_tripla(x:float, a1:float, b1:float, a2:float, b2:float, a3:float, b3:float):
    if x < 95:
        return a1*x + b1
    elif x < 225:
        return a2*x + b2
    else:
        return a3*x + b3

def simples_multipla(x, a1, b1, a2, b2, a3, b3, a4, b4, a5, b5, a6, b6, a7, b7, a8, b8):
    if x < 25:
        return a1*x + b1
    elif x < 50:
        return a2*x + b2
    elif x < 75:
        return a3*x + b3
    elif x < 100:
        return a4*x + b4
    elif x < 125:
        return a5*x + b5
    elif x < 150:
        return a6*x + b6
    elif x < 200:
        return a7*x + b7
    else:
        return a8*x + b8

def quadratica_dupla(x, a1, b1, k1, a2, b2, k2):
    return quadratica_inversa(x, a1, b1, k1) * quadratica_inversa(x, a2, b2, k2)
       

def s2(x, a, b):
    from math import sin
    return sin(x*a) + sin(x*b)

def s(x, a, b, c):
    from math import sin
    return sin(x*(a+1)) * (b+1) + c

if __name__ == "__main__":
    from random import random, seed
    seed(1)
    
##    model_1 = discrete_function(exp, a = 1, k = 1)
##    model_2 = discrete_function(quadratica_inversa, a = 1, b = 1, k = 1)
##    model_3 = discrete_function(quadratica, a = 1, b = 1, k = 1)
##    model_4 = discrete_function(simples, a = 1, b = 1)
##    model_5 = discrete_function(simples_dupla, a1 = 1, b1 = 1, a2 = 1, b2 = 1, limiar = 100)
##    model_6 = discrete_function(simples_tripla, a1 = 1, b1 = 1, a2 = 1, b2 = 1, a3 = 1, b3 = 1)
##    model_7 = discrete_function(quadratica_dupla, a1 = 1, b1 = 1, k1 = 1, a2 = 1, b2 = 1, k2 = 1)
##    model_8 = discrete_function(simples_dupla_suave, a1 = 1, b1 = 1, a2 = 1, b2 = 1)
##
##    x =     [25, 30, 35, 40, 50, 60, 70, 80, 90, 100, 120, 140, 180, 220, 260, 300]
##    curve = [i**((random()+random()+random()+random()+random())/25 + 1.45) + random() * i/5 - i/10 for i in x]#[31, 43, 48, 56, 72, 84, 94, 102, 110, 124, 135, 168, 255, 307, 340, 406]
##
##    best_model = adjust_sample_on(curve = curve, x = x,
##                                  models = [model_1, model_2, model_3, model_4, model_5, model_6, model_7, model_8], 
##                                  initial_value = 0.1,
##                                  times = 10,
##                                  plot = True)

##    x = [i * 0.25 for i in range(10)]
##    curve = [s2(i, a = 3, b = 7) for i in x]
##
##    model = discrete_function(s2, a = 1, b = 1)
##    best_model = adjust_sample_on(curve = curve, x = x,
##                                  models = [model],
##                                  times = 8,
##                                  initial_value = 0.2,
##                                  plot = True)

##    best_model.plot([0,10])
##    best_model[0:10].plot()
    
##    x = [i for i in range(20)]
##    curve = [simples(i, a = 3, b = 7) + simples_dupla(i, a1 = 1, b1 = 2, a2 = 3, b2 = 4, limiar = 0.5) for i in x]
##
##    model_h1 = discrete_function(simples, a = 1, b = 1)
##    model_h2 = discrete_function(simples_dupla, a1 = 1, b1 = 1, a2 = 1, b2 = 1, limiar = 1)
##    model_h = model_h1 + model_h2
##    model_h.name = "mixture"
##    print(model_h)
##    
##    best_model = adjust_sample_on(curve = curve, x = x,
##                                  models = [model_h],
##                                  times = 8,
##                                  initial_value = 0.2,
##                                  plot = True)



##
##    def t1(x, a, b, c):
##        return (x*a + b)+c
##    def t2(x, d):
##        return x+d
##    model1 = discrete_function(t2)
##    model = discrete_function(t1) + discrete_function(t2)
##    curve = [t1(i, a = 3, b = 9, c = 5) + t2(i, d = 7) for i in range(20)]
##    b = adjust_sample_on(curve = curve, x = [i for i in range(20)],
##                         models = [model1, model],
##                         plot = True)


    from math import sin, cos
    def s(x, sa): #sin
        return sin(x*sa)

    def c(x, ca, **args): #cos
        return cos(x*ca)

    def linear(x, la, lb, **args):
        return la + x*lb

    
    model_1 = Discrete_function(s)
    model_2 = Discrete_function(c)

    final_model = model_1 + model_2 

    x = [i * 0.1 for i in range(10)]
    curve = [s(i, sa = 3) + c(i, ca = 4) for i in x]

    best_model = adjust_sample_on(curve = curve, x = x,
                                  models = [final_model],
                                  times = 15,
                                  initial_value = 0.1,
                                  plot = False)

    
    model_1 = Discrete_function(s)
    model_2 = Discrete_function(c)
    model_3 = Discrete_function(linear)

    final_model = (model_1 + model_2 - 1) * (model_3/3)

    x = [i * 0.1 for i in range(10)]
    curve = [(s(i, sa = 3) + c(i, ca = 20) - 1) * (linear(i, la = 12, lb = 40)/3) for i in x]

    best_model = adjust_sample_on(curve = curve, x = x,
                                  models = [final_model],
                                  times = 15,
                                  initial_value = 0.1,
                                  plot = True)
     
