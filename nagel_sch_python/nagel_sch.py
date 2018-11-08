#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random
import time
from os import system, name 


def clear():
    """
    Czyszczenie ekranu

    Funkcja przystosowana do Windowsa i Linuxa/MacOSX
    :return:
    """
    # for windows
    if name == 'nt': 
        _ = system('cls') 
  
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 


N = 80
vmax = 5
d = 0.3
num_of_vehicles = d * N

cells = np.zeros(80).astype(int)
cells = cells-1

# wypelnianie drogi losowymi samochodami

for i in range(0, cells.size):
   if i % int(N/num_of_vehicles) == 0:
        cells[i] = random.randint(0, vmax)

# lista wszystkich iteracji
# symulacja offline, najpierw wszystko
# wyliczane, a na koncu wyswietlana wizualizacja
iterations = []

for x in range(0, 500):
    # zwiekszanie predkosci
    cells[cells >= 0] = cells[cells >= 0] + 1
    cells[cells > vmax] = vmax

    # hamowanie
    for i in np.nonzero(cells >= 0)[0]:
        v = cells[i]
        for k in range(1, v+1):
            if cells[(i+k)%N] != -1:
                cells[i] = k-1
                break
            
    # losowe hamowanie
    for i in np.nonzero(cells > 0)[0]:
        if random.random() < 0.3:
            cells[i] = cells[i] - 1
             
    # przemieszczanie
    for i in np.nonzero(cells > 0)[0]:
        v = cells[i]
        j = (i+v)%N
        cells[j] = cells[i]
        cells[i] = -1

    # dodanie drogi do listy iteracji
    iterations.append(np.copy(cells))

clear()
# wizualizacja
for i in iterations:
    road = ""
    for j in i:
        if j == -1:
            road += "-"
        else:
            road += str(j)
    clear()
    print(road)
    print(road)
    time.sleep(1)