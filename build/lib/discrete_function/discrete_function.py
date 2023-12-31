from random import random
import inspect

class probability:
    def __init__(self, value, start:int = 0):
        if type(value) != list:
            value = [value]
        self.value = value
        self.start = start

    def plot(self, iterations = None, **keyargs):
        if len(self.value) < 4:
            return None
        
        import matplotlib.pyplot as plt
        from scipy.interpolate import interp1d

        def v_1(x):
            return x[0]
        def v_2(y):
            return y[1]

        def to_clean(xy, limit:list):
            xy_n = []
            for iten in xy:
                if limit[0] <= iten[0] <= limit[1]:
                    xy_n.append(iten)
            return xy_n
            

        if iterations == None:
            iterations = 8 + int(50/(len(self.value)+3))

        x = [self.start + i/(iterations) for i in range((len(self.value) - 1) * iterations + 1)]        
        y = interp1d([self.start + i for i in range(len(self.value))], self.value, kind='cubic')
        
        plt.plot(x, y(x))

        plt.xlabel('x')
        plt.ylabel('y')

        plt.show()

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

    def __len__(self):
        return len(self.value)

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
        if args == () and keyargs == {}:
            argspec = inspect.getfullargspec(function)
            self.args = args
            self.keyargs = {keyargs_:1 for keyargs_ in argspec.args}
            del self.keyargs["x"]
        else:
            self.args = args
            self.keyargs = keyargs
        self.function = function
        self.values = None
        self.value = None
        self.enough = None
        self.value_accumulated = None
        self.name = function.__name__
        self.error = None
        self.initial_value = 1

    def find(self, x:int = 0):
        if type(x) == int or type(x) == float:
            if type(self.value) == probability:
                return self.function(x, *self.args, **self.keyargs)
            else:
                try:
                    return probability(self.function(x, *self.args, **self.keyargs))
                except TypeError:
                    raise Exception("Add **args to the mixed function parameters")
        elif type(x) == slice:
            if x.start == None:
                x.start = 0
            if x.stop == None:
                x.stop = (index.start + 1)*2
            if type(self.value) == probability:
                return [self.function(i, *self.args, **self.keyargs) for i in range(x.start, x.stop + 1)]
            else:
                return probability([self.function(i, *self.args, **self.keyargs) for i in range(x.start, x.stop + 1)], start = x[0])
        elif type(x) == list or type(x) == tuple:
            if type(self.value) == probability:
                return [self.function(i, *self.args, **self.keyargs) for i in x]
            else:
                return probability([self.function(i, *self.args, **self.keyargs) for i in x], start = x[0])
            
            

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

    def adjust_to_curve(self, name_param:str = None, curve:list = None, x:list = None, max_iterations:int = 100, initial_value:float = 1, plot:bool = False, times:int = 1, print_details:bool = True):
        """
        curve has to be a list with values f(x) = y where x starts
        at 0 and goes to the end of the list being real numbers.
        
        param is a positive number.
        """

        if x == None:
            x = [i for i in range(len(curve))]

        if type(name_param) == list:
            params_variables = {}
            for t in range(times):
                if print_details:
                    print("-" * 15 + str(t) +  "-" * 15)
                for name in name_param:
                    if print_details:
                        print(f"Finding parameters for the {name}:")
                    parans = self.adjust_to_curve(name_param = name,
                                                  curve = curve,
                                                  x = x,
                                                  max_iterations = max_iterations,
                                                  initial_value = initial_value,
                                                  plot = plot)
                    if print_details:
                        print(f"Lower Limit = {parans[0]}\nUpper Limit = {parans[1]}\n")
                    params_variables[name] = parans

            if int(min(params_variables.values())[0] * 2) != initial_value and int(min(params_variables.values())[0] * 2) >= 1:
                v = int(min(params_variables.values())[0] * 2)
                m_v = int(max(params_variables.values())[1]/v * 2.72)
                if print_details:
                    print(f"Recommended value for initial_value = {v}\nRecommended value for max_iterations = {m_v}")
            elif int(min(params_variables.values())[0] * 2) != initial_value and 0.2 <= min(params_variables.values())[0] * 2 < 1:
                v = int(min(params_variables.values())[0] * 200)/100
                m_v = int(max(params_variables.values())[1]/v * 2.72)
                self.initial_value = v
                if print_details:
                    print(f"Recommended value for initial_value = {v}\nRecommended value for max_iterations = {m_v}")
            return params_variables
            
        else:
            jump = initial_value
            param_0, param_1 = 0, jump

            self.keyargs[name_param] = param_0
            self.values = [self.find(i) for i in x]
            dif_0 = rms(self.values, curve)

            self.keyargs[name_param] = param_1
            self.values = [self.find(i) for i in x]
            dif_1 = rms(self.values, curve)

            op = 0
            while op < max_iterations and param_0 != param_1:
                if dif_0 < dif_1:
                    param_1 = (param_0 + param_1)/2
                    jump /= 2
                    
                    self.keyargs[name_param] = param_1
                    self.values = [self.find(i) for i in x]
                    dif_1 = rms(self.values, curve)
                else:
                    param_0, param_1 =(param_0 + param_1)/2, param_1 + jump

                    self.keyargs[name_param] = param_0
                    self.values = [self.find(i) for i in x]
                    dif_0 = rms(self.values, curve)                
                    self.keyargs[name_param] = param_1
                    self.values = [self.find(i) for i in x]
                    dif_1 = rms(self.values, curve)
                op += 1
            self.error = max(dif_0, dif_1)

            if plot:
                import matplotlib.pyplot as plt
                l_x = len(curve)
                if x == None:
                    x = [i for i in range(l_x)]
                y1 = curve
                self.keyargs[name_param] = param_0
                y2_ = [self.find(i) for i in x]
                self.keyargs[name_param] = param_1
                y3_ = [self.find(i) for i in x]
                
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

                plt.plot(x, y2, label = f'{name_param} = {str(param_0)[:6]}')
                plt.plot(x, y3, label = f'{name_param} = {str(param_1)[:6]}')

                plt.scatter(x, y1, color='red', marker='o', label='Observation')

                plt.xlabel('x')
                plt.ylabel('y')
                plt.title(f'Adjusting Observations in the Function {self.name}')
                plt.legend()

                plt.show()

            if dif_0 < dif_1:
                self.keyargs[name_param] = param_0
            else:
                self.keyargs[name_param] = param_1

            return param_0, param_1

    def plot(self, x_limits:list = None, **keyargs):
        import matplotlib.pyplot as plt

        self.random(1)
        if x_limits == None:
            x_limits = [0, self.enough]
            
        x = [i for i in range(x_limits[0], x_limits[1] + 1)]

        try:
            plt.plot(x, self.find(x).value.copy())
        except:
            plt.plot(x, self.find(x))

        plt.xlabel('x')
        plt.ylabel('y')
        
        plt.title(f'{self.name}')

        plt.show()

    def random(self, times:int = 1, random = random):
        n = 4
        accumulate = self.accumulated(0, n)
        while accumulate < 0.999 and n < 2**10:
            n *= 2
            accumulate = self.accumulated(0, n)
            self.enough = n

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
            index = [i for i in range(start, stop + 1)]
        if type(self.find(index)) == probability:
            return self.find(index)
        else:
            return probability(self.find(index), start = start)

    def __add__(self, obj):
        if type(obj) == discrete_function:
            return discrete_function(lambda x, **args: self.function(x, **args) + obj.function(x, **args),
                                     **self.keyargs,
                                     **obj.keyargs)
        elif type(obj) == float or type(obj) == int:
            return discrete_function(lambda x, **args: self.function(x, **args) + obj,
                                     **self.keyargs)

    def __sub__(self, obj):
        if type(obj) == discrete_function:
            return discrete_function(lambda x, **args: self.function(x, **args) - obj.function(x, **args),
                                     **self.keyargs,
                                     **obj.keyargs)
        elif type(obj) == float or type(obj) == int:
            return discrete_function(lambda x, **args: self.function(x, **args) - obj,
                                     **self.keyargs)

    def __truediv__(self, obj):
        if type(obj) == discrete_function:
            return discrete_function(lambda x, **args: self.function(x, **args) / obj.function(x, **args) if obj.function(x, **args) != 0 else 0,
                                     **self.keyargs,
                                     **obj.keyargs)
        elif type(obj) == float or type(obj) == int:
            return discrete_function(lambda x, **args: self.function(x, **args) / obj,
                                     **self.keyargs)

    def __mul__(self, obj):
        if type(obj) == discrete_function:
            return discrete_function(lambda x, **args: self.function(x, **args) * obj.function(x, **args),
                                     **self.keyargs,
                                     **obj.keyargs)
        elif type(obj) == float or type(obj) == int:
            return discrete_function(lambda x, **args: self.function(x, **args) * obj,
                                     **self.keyargs)
    
    def __pow__(self, obj):
        if type(obj) == discrete_function:
            return discrete_function(lambda x, **args: self.function(x, **args) ** obj.function(x, **args),
                                     **self.keyargs,
                                     **obj.keyargs)
        elif type(obj) == float or type(obj) == int:
            return discrete_function(lambda x, **args: self.function(x, **args) ** obj,
                                     **self.keyargs)

            
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

def adjust_sample_on(curve, models, x:list = None, initial_value:float = 0.25, max_iterations:int = 20, times:int = 6, plot:bool = False, print_details:bool = False):
    from copy import deepcopy
    
    best_model = (models[0], 999999999999)
    original = initial_value
    
    for model in models:
        best_temporary_model = (models[0], 999999999999)
        initial_value = original
        for i in range(times - 1):
            initial_value *= 2
            for _ in range(times):
                model.adjust_to_curve(name_param = list(model.keyargs),
                                      curve = curve,
                                      x = x,
                                      initial_value = initial_value,
                                      plot = False,
                                      times = 1,
                                      max_iterations = max_iterations,
                                      print_details = print_details)
                if model.error < best_model[1]:
                    best_model = (deepcopy(model), deepcopy(model.error))
                if model.error < best_temporary_model[1]:
                    best_temporary_model = (deepcopy(model), deepcopy(model.error))
                    

        if plot:
            import matplotlib.pyplot as plt
            
            if x == None:
                x = [i for i  in range(len(curve))]

            x_1 = set([i for i in range(int(x[0]), int(x[-1]))])
            x_2 = set(x)
            
            plt.plot(sorted(x_1 | x_2), best_temporary_model[0][list(sorted(x_1 | x_2))].value, label = f'Function')
            plt.scatter(x, curve, color='red', marker='o', label = 'Observation')

            plt.xlabel('x')
            plt.ylabel('y')
            plt.title(f'Best Model of {best_temporary_model[0].name}, ERROR: {best_temporary_model[1]}')
            plt.legend()

            plt.show()
        

    print("Best Model:")
    print(best_model[0])
    return best_model[0]

def b_(pont_1:list, pont_2:list, porc:float):  
    return [(pont_2[0] - pont_1[0])* porc + pont_1[0],
            (pont_2[1] - pont_1[1])* porc + pont_1[1]]#posição do ponto

def bezier(pont_1:list, pont_2:list, pont_3:list, prec:int):
    pont = []
    for i in range(prec):
        n = 1/(prec-1) * (i)
        pont.append(b_(b_(pont_1, pont_2 , n), b_(pont_2, pont_3 , n), n))
    return pont

def smooth_curve(p1:list, p2:list, p3:list, p4:list, iterations:int = 4):
    f1 = [p2[1]-p1[1], p1[1] - (p2[1]-p1[1]) * p1[0]]
    f2 = [p4[1]-p3[1], p3[1] - (p4[1]-p3[1]) * p3[0]]

    try:
        cx = -(f1[1] - f2[1])/(f1[0] - f2[0])
    except ZeroDivisionError:
        cx = 0
    cy = f1[0] * cx + f1[1]
    c = [cx, cy]

    return bezier(*sorted((p2, c, p3), key=lambda x: x[0]), iterations)

Discrete_function = discrete_function
