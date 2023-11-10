import numpy as np
import random

def det_m(n1, n2, dim):
    '''Generate square matrix'''
    # n1 - minor number in matrix
    # n2 - grater number in matrix
    # dim - dimension of the matrix (m = n = dim, square matrix)

    m1 = np.random.randint(n1, n2, size=(dim, dim))
    # m1 = np.random.randint(0, 19, size=(2, 2))
    det_m1 = round(np.linalg.det(m1))

    return m1, det_m1




def r_sum(n1: int, n2: int, r_len: int):
    # Вычисление суммы цифр
    #

    # Генератор ряда
    # r_len = 8
    row_num = ''
    row_num_summ = 0

    for i in range(r_len):
        # t = random.randint(0, 9)
        t = random.randint(n1, n2)
        row_num += str(t)
        row_num_summ += t

    return row_num, row_num_summ