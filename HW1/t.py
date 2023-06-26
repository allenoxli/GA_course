
import math

# x1 =  0.87494
# x2 = 0.81244
# def tmp(x1, x2):
#     left_part = (x1**2 + x2**2)**0.25
#     right_part = math.sin(50*(x1**2 + x2**2)**0.1)**2 + 1
#     interval = 6.10352e-05
#     return left_part * right_part


# def eval(x1, x2):
#     return ((x1**2 + x2**2)**0.25) * (math.sin(50 * (x1**2 + x2**2)**0.1)**2 + 1)

# print(tmp(x1, x2))
# print(eval(x1, x2))

n_bit = 0
precision = 0.0001
max_bound, min_bound = 1, 0
tmp = max_bound - min_bound
while (precision < tmp):
    tmp /= 2
    n_bit += 1

print(n_bit)

print(((max_bound - min_bound)/(2**14 - 1)) < precision)