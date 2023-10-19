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

def t_g(x, a, b, k):
    resp = -a*(x - k)**2 + b
    if resp < 0:
        return 0
    return resp

def func_rodrigo(y, lambda_, sigma_2):        
    
    def func_b(y):
        return gamma(-lambda_/(sigma_2 - 1) + 1) / (gamma(y + 1) * gamma(-lambda_/(sigma_2 - 1) - y + 1)) * (1 - sigma_2)**(y) * sigma_2 ** (-lambda_/(sigma_2 - 1) - y)

    def D():
        resp = 0
        for i in range(0, int(-lambda_/(sigma_2 - 1) + 1)):
            resp += func_b(i)
        return resp
    
    if y > 0:
        resp = func_rodrigo(0, lambda_, sigma_2)
        for j in range(1, y + 1):
            try:
                resp *= (lambda_ + (sigma_2 - 1)*(j-1))/(sigma_2*j)
            except ZeroDivisionError:
                pass

        return resp

    elif y == 0 and sigma_2 == 1:
        return 2.71828182**(-lambda_)

    elif y == 0 and sigma_2 > 1:
        return sigma_2 ** (-(lambda_)/(sigma_2 - 1))

    elif y == 0 and 0 < sigma_2 < 1:
        return sigma_2 ** (-(lambda_)/(sigma_2 - 1)) * 1/D()

    else:
        return 0

def polinomio(x:int, b1 = 1, b2 = 1, c = 1):
    return (b1*(x/(c + 1))**2 - (b2/(c+b1+1))*x )

def poisson_dupla(x, mi_1, mi_2, p):
    return poisson(x, mi_1)*p + poisson(x, mi_2)*(1 - p)**2
        

def poisson_tripla(x, mi_1, mi_2, mi_3):
    return poisson(x, mi_1)/3 + poisson(x, mi_2)/3 + poisson(x, mi_3)/3


if __name__ == "__main__":
    from discrete_function import discrete_function, adjust_sample_on
    from random import random, seed
    seed(2023)
    
##    funcao = discrete_function(poisson, mi = 5)
##    print(funcao.keyargs)
##    print(funcao.find(x = 2))
##    print(funcao.accumulated(0, 10))
##    curva = [poisson(i, mi = 7.4215) + random()*0.05-0.025 for i in range(0, 20)]
##    curva = list(map(lambda x: 0 if x < 0 else x, curva))
##    limites = funcao.adjust_to_curve(name_param = "mi",
##                                     curve = curva,
##                                     initial_value = 1,
##                                     plot = True)
##    print(limites)
##
##
##    func = discrete_function(func_rodrigo, lambda_ = 3, sigma_2 = 0.5)
##    print(func.find([0, 9]))
##    
####    func.adjust_to_curve(name_param = "lambda_",
####                                   curve = curva,
####                                   initial_value = 1,
####                                   plot = True)
####
####    func.adjust_to_curve(name_param = "sigma_2",
####                                   curve = curva,
####                                   initial_value = 1,
####                                   plot = True)
##
##    p = func.adjust_to_curve(name_param = ["lambda_", "sigma_2"],
##                         curve = curva,
##                         initial_value = 1,
##                         plot = True,
##                         times = 2,
##                         max_iterations = 12)
##    
##    func.random()
##
##    print(func)
##
##    print(func[1:3] | func[0:6])

    curva = [poisson_tripla(i, mi_1 = 20.34, mi_2 = 10.87, mi_3 = 1.05) for i in range(0, 30)]
    modelo = discrete_function(poisson_tripla, mi_1 = 1, mi_2 = 1, mi_3 = 1)

##    modelo.plot([0,30])    
##    p = modelo.adjust_to_curve(name_param = ['mi_1', 'mi_2', 'mi_3'],
##                         curve = curva,
##                         initial_value = 2,
##                         plot = False,
##                         times = 6,
##                         max_iterations = 27)
##    modelo[1:15].plot()
##    modelo.plot([1,15])

    curva = [normal(i, mi = 6.74, sigma = 4.25) + random() * 0.04 - 0.02 for i in range(0, 15)]
    
    model_1 = discrete_function(poisson, lambda_ = 1)
    model_2 = discrete_function(normal, sigma = 1, mi = 1)
    model_3 = discrete_function(t_g, a = 1, b = 1, k = 1)

    best_model = adjust_sample_on(curva, [model_1, model_2, model_3],
                                  plot = True)


    

