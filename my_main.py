import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm as cm
import pandas as pd
import seaborn as sns

import re
import math
from functools import reduce

"""arr_average is a function that return the average (an arrow function)
    previous is our accumulator. It will accumulate our sum as our function works. 
   current is the current value being processed.
   The second parameter of the reduce method is the initial value we wish to use. 
   We’ve set our initial value to zero which allows us to use 
   empty arrays with our arr_average functions."""


def arr_average(my_list):
    return reduce((lambda previous, current: previous + current), my_list, 0) / len(my_list)


# Uses the same logic as the arr_average function but calculate the variance of a given array
def arr_variance(my_list):
    return reduce((lambda previous, current: previous + (current ** 2)), my_list, 0) / len(my_list)


def cov(x, y):
    n = len(x)
    xy = [x[i] * y[i] for i in range(n)]
    mean_x = arr_average(x)
    mean_y = arr_average(y)
    return (sum(xy) - n * mean_x * mean_y) / float(n)


def draw_mat(text, my_mat):
    top = text
    for i in range(num_of_variables):
        top += (' var{0} |'.format(i))
    print(top)
    my_index = 0
    for my_cov in my_mat:
        print('var{0} '.format(my_index), *my_cov, sep='| ')
        my_index += 1


def correlation_matrix(df):
    from matplotlib import pyplot as plt
    from matplotlib import cm as cm

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    cmap = cm.get_cmap('jet', 30)
    cax = ax1.imshow(df, interpolation="nearest", cmap=cmap)
    ax1.grid(True)
    plt.title('Abalone Feature Correlation')
    labels = ['Var 1', 'Var 2', 'Var 3', ' Var 4', 'Var 5', 'Var 6', ]
    ax1.set_xticklabels(labels, fontsize=8)
    ax1.set_yticklabels(labels, fontsize=8)
    # Add colorbar, make sure to specify tick locations to match desired ticklabels
    fig.colorbar(cax, ticks=[.75, .8, .85, .90, .95, 1])
    plt.show()


# "height";"weight";"age";"male"
# open the text file
text_file = open('source1.txt', 'r', encoding='utf8')
raw_data = text_file.read().split('\n')
raw_data = [re.sub(r"\s\s+", " ", data) for data in raw_data]
raw_data = list(filter(bool, raw_data))  # fastest
print('Raw Data : ', raw_data)

individuals = [line.split(' ') for line in raw_data]
individuals = np.array(individuals, dtype=int)  # This is a numpy integer array
print('Individuals : ', individuals)

num_of_individuals = len(individuals)
print('Number of individuals : ', num_of_individuals)

num_of_variables = len(individuals[0])
print('Number of variables : ', num_of_variables)

variables = list(zip(*individuals))
print('Variables : ', variables)

average = [arr_average(current_variable) for current_variable in variables]
print('Average : ', average)

variance = [arr_variance(current_variable) for current_variable in variables]
variance = [value[0] - value[1] ** 2 for value in list(zip(variance, average))]
print('Variance : ', variance)

# ecart type
deviation = [math.sqrt(value) for value in variance]
print('Deviation : ', deviation)

covariance = []
for previous_ in variables:
    temp = []
    for current_ in variables:
        temp.append((cov(previous_, current_)))
    covariance.append(temp)

print('Covariance', covariance)
draw_mat('Covariance', covariance)

correlation = []
for previous_key, previous_ in enumerate(variables):
    temp = []
    for current_key, current_ in enumerate(variables):
        temp.append((cov(previous_, current_) / (deviation[previous_key] * deviation[current_key])))
    correlation.append(temp)

print('Correlation', correlation)
draw_mat('Correlation', correlation)

# correlation_matrix(correlation)
my_data = pd.DataFrame(individuals)
# print(my_data.corr())
# calculate the correlation matrix
corr = my_data.corr()
# print(corr)
# "height";"weight";"age";"male"
var_names = ['height', 'weight', 'age']
# plot the heatmap
cmap = cm.get_cmap('jet', 30)
sns.heatmap(correlation, xticklabels=var_names, yticklabels=var_names, cmap=cmap)
plt.show()
