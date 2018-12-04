"""
Model ten jest identyczny jak model nagel_sch_m.py z parametrem długosci samochodu = 1
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import random

import data_presentation as dp

def nagel_sch(N, d, vmax, num_of_iterations=30):
    """
    Implementacja modelu nagel_sch

    :param N: dlugosc drogi
    :param d: gestosc (ile % pojazdow na drodze, np. 0.5 to polowa
    drogi zajeta przez pojazdy)
    :param vmax: predkosc maksymalna
    :param num_of_iterations: ile iteracji symulacji (jednostek czasu)

    :return: (flow, iterations) - flow to wektor zbadanych przepustowosci drogi (pojazdow/s), iterations
    to lista wektorow, gdzie kazdy wektor to reprezentacja drogi. Iterations sluzy do wizualizacji symulacji, flow
    sluzy do budowania diagramu fundamentalnego
    """

    num_of_vehicles = d * N

    cells = np.zeros(N).astype(int)
    cells = cells - 1

    # lambda do znalezienia indeksow gdzie wstawic samochody
    # m to liczba elementow do wstawienia do macierzy
    # n to dlugosc wektora
    # zwraca indeksy wektora pod ktore nalezy wstawic elementy
    # aby mialy w miare jednakowe odstepy
    f = lambda m, n: [i * n // m + n // (2 * m) for i in range(m)]
    vehicles_indices = f(np.ceil(num_of_vehicles).astype(int), N)
    vehicles_speeds = np.random.randint(0, vmax, N)

    # wypelniamy droge losowymi samochodami (predkosciami)
    vehicles_speeds_index = 0
    for index in vehicles_indices:
        cells[index] = vehicles_speeds[vehicles_speeds_index]
        vehicles_speeds_index += 1

    # lista wszystkich iteracji
    # symulacja offline, najpierw wszystko
    # wyliczane, a na koncu wyswietlana wizualizacja
    iterations = []
    
    flow_sum = 0
    for x in range(0, num_of_iterations):
        # zwiekszanie predkosci
        cells[cells >= 0] = cells[cells >= 0] + 1
        cells[cells > vmax] = vmax

        # hamowanie
        for i in np.nonzero(cells >= 0)[0]:
            v = cells[i]
            for k in range(1, v + 1):
                if cells[(i + k) % N] != -1:
                    cells[i] = k - 1
                    break

        # losowe hamowanie
        for i in np.nonzero(cells > 0)[0]:
            if random.random() < 0.3:
                cells[i] = cells[i] - 1

        # przemieszczanie
        for i in np.nonzero(cells > 0)[0]:
            v = cells[i]
            j = (i + v) % N
            cells[j] = cells[i]
            cells[i] = -1

        # dodanie drogi do listy iteracji
        iterations.append(np.copy(cells))
        
        average_velocity = np.sum(cells[cells >= 0])/np.sum(cells >= 0)
        flow_sum += d * average_velocity

    # liczymy sredni flow ze wszystkich iteracji (w calym czasie symulacji)
    average_flow = flow_sum/num_of_iterations
    return average_flow, iterations

################
# MAIN
################


def main():
    density_arr = np.arange(0.05, 0.6, 0.01)
    flow_arr = np.copy(density_arr)

    # badamy model dla roznych gestosci ruchu
    for i in range(0, len(flow_arr)):
        [flow, iterations] = nagel_sch(10000, density_arr[i], 5)
        flow_arr[i] = flow

    dp.fundamental_diagram(flow_arr, density_arr)

    [flow, iterations] = nagel_sch(80, 0.3, 5, 120)
    # image_visualisation(iterations)
    dp.offline_visualisation_one_lane(iterations)


if __name__ == "__main__":
    main()
