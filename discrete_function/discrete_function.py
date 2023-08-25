from random import random

class probability:
    def __init__(self, value):
        if type(value) != list:
            value = [value]
        self.value = value

    def __or__(self, other):
        return probability(sum(self.value)/sum(other.value))

    def __div__(self, other):
        if len(self.value) == len(other.value) == 1:
            return self.value[0]/other.value[0]

    def __repr__(self):
        if type(self.value[0]) == list:
            self.value = self.value[0]
        return str(self.value)

    def __str__(self):
        if type(self.value[0]) == list:
            self.value = self.value[0]
        return str(self.value)

    def __iadd__(self, value):
        if type(value) == int or type(value) == float:
            return probability(sum(self.value) + value)
        elif type(value) == probability:
            return probability(sum(self.value) + sum(value.value))

    def __add__(self, value):
        if type(value) == int or type(value) == float:
            return probability(sum(self.value) + value)
        elif type(value) == probability:
            return probability(sum(self.value) + sum(value.value))

    def __isub__(self, value):
        if type(value) == int or type(value) == float:
            return probability(sum(self.value) - value)
        elif type(value) == probability:
            return probability(sum(self.value) - sum(value.value))

    def __sub__(self, value):
        if type(value) == int or type(value) == float:
            return probability(sum(self.value) - value)
        elif type(value) == probability:
            return probability(sum(self.value) - sum(value.value))

    def __pow__(self, value):
        if type(value) == int or type(value) == float:
            return probability(sum(self.value) ** value)
        elif type(value) == probability:
            return probability(sum(self.value) ** sum(value.value))

    def __lt__(self, value):
        if type(value) == int or type(value) == float:
            return self.value[0] < value
        elif type(value) == probability:
            return self.value[0] < value.value[0]

    def __le__(self, value):
        if type(value) == int or type(value) == float:
            return self.value[0] > value
        elif type(value) == probability:
            return self.value[0] > value.value[0]

    def __eq__(self, value):
        if type(value) == int or type(value) == float:
            return self.value[0] == value
        elif type(value) == probability:
            return self.value[0] == value.value[0]

    def __getitem__(self, index):
        if type(index) == slice:
            start, stop = index.start, index.stop
            if index.start == None:
                start = 0
            if index.stop == None:
                stop = (index.start + 1)*2
            index = [start, stop]
            return probability(self.value[index[0]: index[1]])
        if type(index) == tuple or type(index) == list:
            return probability(self.value[index[0]: index[1]])
        return probability(self.value[index])
            

    def append(self, value):
        self.value.append(value)

class discrete_function:
    def __init__(self, function = None, *args, **keyargs):
        self.args = args
        self.keyargs = keyargs
        self.function = function
        self.values = None
        self.value = None
        self.value_accumulated = None
        self.name = function.__name__

    def find(self, x:int = 0):
        if type(x) == int:
            if type(self.value) == probability:
                return self.function(x, *self.args, **self.keyargs)
            else:
                return probability(self.function(x, *self.args, **self.keyargs))
        if type(x) == list or type(x) == tuple:
            if type(self.value) == probability:
                return [self.function(i, *self.args, **self.keyargs) for i in range(x[0], x[1] + 1)]
            else:
                return probability([self.function(i, *self.args, **self.keyargs) for i in range(x[0], x[1] + 1)])
            

    def accumulated(self, inferior_limit = 0, upper_limit = 10):
        self.values = [self.find(i) for i in range(inferior_limit, upper_limit + 1)]

        self.value = 0
        self.value_accumulated = []
        for value in self.values:
            #print(self.value, value, type(self.value), type(value))
            self.value = value + self.value
            self.value_accumulated.append(self.value)

        if type(self.value) == probability:
            return self.value
        else:
            return probability(self.value)

    def adjust_to_curve(self, name_param:str = None, curve:list = None, max_iterations = 100, initial_value = 1, plot = False, times:int = 1):
        """
        curve has to be a list with values f(x) = y where x starts
        at 0 and goes to the end of the list being real numbers.
        
        param is a positive number.
        """

        if type(name_param) == list:
            params_variables = {}
            for t in range(times):
                print("-" * 15 + str(t) +  "-" * 15)
                for name in name_param:
                    print(f"Finding parameters for the {name}:")
                    parans = self.adjust_to_curve(name_param = name,
                                                  curve = curve,
                                                  max_iterations = max_iterations,
                                                  initial_value = initial_value,
                                                  plot = plot)
                    print(f"Lower Limit = {parans[0]}\nUpper Limit = {parans[1]}\n")
                    params_variables[name] = parans
            print(f"Recommended value for initial_value = {int(min(params_variables.values())[0] * 2)}")
            return params_variables
            
        else:
            jump = initial_value
            param_0, param_1 = 0, jump

            self.keyargs[name_param] = param_0
            self.values = [self.find(i) for i in range(len(curve))]
            dif_0 = rms(self.values, curve)

            self.keyargs[name_param] = param_1
            self.values = [self.find(i) for i in range(len(curve))]
            dif_1 = rms(self.values, curve)

            op = 0
            while op < max_iterations and param_0 != param_1:
                if dif_0 < dif_1:
                    param_1 = (param_0 + param_1)/2
                    jump /= 2
                    
                    self.keyargs[name_param] = param_1
                    self.values = [self.find(i) for i in range(len(curve))]
                    dif_1 = rms(self.values, curve)
                else:
                    param_0, param_1 =(param_0 + param_1)/2, param_1 + jump

                    self.keyargs[name_param] = param_0
                    self.values = [self.find(i) for i in range(len(curve))]
                    dif_0 = rms(self.values, curve)                
                    self.keyargs[name_param] = param_1
                    self.values = [self.find(i) for i in range(len(curve))]
                    dif_1 = rms(self.values, curve)

                #print(param_0, param_1, op)
                #print(dif_0, dif_1)
                op += 1

            if plot:
                import matplotlib.pyplot as plt
                l_x = len(curve)
                x = [i for i in range(l_x)]
                y1 = curve
                self.keyargs[name_param] = param_0
                y2_ = [self.find(i) for i in range(l_x)]
                self.keyargs[name_param] = param_1
                y3_ = [self.find(i) for i in range(l_x)]
                
                y2 = []
                if type(y2_[0]) == probability:
                    for sublist in y2_:
                        y2.append(sublist.value[0])
                else:
                    y2 = y2_

                y3 = []
                if type(y3_[0]) == probability:
                    for sublist in y3_:
                        y3.append(sublist.value[0])
                else:
                    y3 = y3_

                plt.plot(x, y2, label = f'{name_param} = {str(param_0)[:4]}')
                plt.plot(x, y3, label = f'{name_param} = {str(param_1)[:4]}')

                # Crie um gráfico de pontos
                plt.scatter(x, y1, color='red', marker='o', label='Observation')

                # Adicione rótulos e título ao gráfico
                plt.xlabel('x')
                plt.ylabel('y')
                plt.title('Adjusting Observations in the Function')
                plt.legend()

                # Mostre o gráfico
                plt.show()

            if dif_0 < dif_1:
                self.keyargs[name_param] = param_0
            else:
                self.keyargs[name_param] = param_1

            return param_0, param_1

    def random(self, times = 1, random = random):
        n = 4
        accumulate = self.accumulated(0, n)
        while accumulate < 0.999 and n < 2**10:
            n *= 2
            accumulate = self.accumulated(0, n)

        k = []
        for i in range(times):
            n_random = random()
            n = 1
            while self.value_accumulated[n] < n_random:
                n += 1
            k.append(n)
        return k[0] if times == 1 else k

    def __str__(self):
        return f"Function: {self.name}\nAll args: {self.args} {self.keyargs}"

    def __getitem__(self, index):
        if type(index) == slice:
            start, stop = index.start, index.stop
            if index.start == None:
                start = 0
            if index.stop == None:
                stop = (index.start + 1)*2
            index = [start, stop]
        if type(self.find(index)) == probability:
            return self.find(index)
        else:
            return probability(self.find(index))

def rms(curve_1:list, curve_2:list):
    """
    root mean square error
    """
    resp = 0
    if len(curve_1) != len(curve_2):
        raise DifferentListSizesError("Different list sizes")
    for a, b in zip(curve_1, curve_2):
        resp = (a - b)**2 + resp
    return resp    
