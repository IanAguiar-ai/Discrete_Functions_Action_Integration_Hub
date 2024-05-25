# Discrete_Functions_Action_Integration_Hub
HUB that adds higher-level functionalities to discrete functions created from scratch.

## To download:

```
pip install git+https://github.com/IanAguiar-ai/Discrete_Functions_Action_Integration_Hub
```

##Operation

### Summary:

```
class
 └─discrete_funcion (Discrete_function, Df)
    ├─find
    ├─accumulated
    ├─adjust_to_curve
    ├─plot
    ├─sample
    ├─evaluate
    ├─residual
    ├─-----(other less relevant functions(self))
    └─-----(__special_methods__)
functions
 ├─adjust_sample_on
 ├─sample_of
 ├─accumulated_sample
 └─continuous_accumulation
```

### Operation:

```
.-----.                       
|curve|                       
'.----'                       
.'--------------------------. 
|           model           | 
'.----------------.--.--.--.' 
.'---------------.|  |  |  |  
|adjust_sample_on||  |  |  |  
'----------------'|  |  |  |  
.-----------.     |  |  |  |  
|probability|     |  |  |  |  
'.----------'     |  |  |  |  
.'----------------'-.|  |  |  
| discrete_function ||  |  |  
'-------------------'|  |  |  
.----.               |  |  |  
|plot|               |  |  |  
'.---'               |  |  |  
.'-------------------'-.|  |  
|      regression      ||  |  
'----------------------'|  |  
.-----------------------'-.|  
|      your_function      ||  
'-------------------------'|  
.--------------------------'-.
|             x              |
'----------------------------'

```
