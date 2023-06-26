from matplotlib import pyplot as plt
from math import sqrt, cos, sin, pi
import random

import numpy as np

def fitness_func(x, y):
    return  80 - x**2 - y**2 + 10*np.cos(2*pi*x) + 10*np.cos(2*pi*y)


 
from mpl_toolkits.mplot3d import Axes3D  #用来给出三维坐标系。

def draw_3D(X, Y, Z):
    figure = plt.figure()

    axes = Axes3D(figure)
    
    axes.plot_surface(X, Y, Z, cmap='rainbow')

    plt.savefig('Q1.png')

def draw_contour(X, Y, Z):
    n = 1000
    x = np.linspace(-0.5, 1.5, n)
    y = np.linspace(-0.5, 1.5, n)
    X, Y = np.meshgrid(x, y)
    #繪製等高線圖
    plt.contourf(X, Y, fitness_func(X, Y), 10, alpha=.6, cmap=plt.cm.jet)
    plt.savefig('Q1_contour.png')


X = np.arange(-0.5, 1.5, 0.01)
Y = np.arange(-0.5, 1.5, 0.01)
X, Y = np.meshgrid(X, Y)
Z = fitness_func(X, Y)

draw_contour(X, Y, Z)
print(fitness_func(0,0))
print(fitness_func(1,1))
print(fitness_func(1,0))
print(fitness_func(0,1))