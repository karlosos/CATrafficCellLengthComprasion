#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zmodyfikowana wersja modelu NagelSch z zmieniona iloscia komorek. Mozliwosc uruchomienia
modelu jako klasycznego modelu NagelSch.
"""

import numpy as np
import random
import comprasion
import matplotlib.pyplot as plt

import data_presentation as dp

def nagel_sch(N, d, vmax, cell_length=7.5, p = 0.3, num_of_iterations=30):
    """
    Implementacja modelu nagel_sch

    :param N: dlugosc drogi
    :param d: gestosc (ile % pojazdow na drodze, np. 0.5 to polowa
    drogi zajeta przez pojazdy)
    :param vmax: predkosc maksymalna
    :param cell_length: jaka dlugosc w metrach ma miec jedna komorka
    :param num_of_iterations: ile iteracji symulacji (jednostek czasu)

    :return: (flow, iterations) - flow to wektor zbadanych przepustowosci drogi (pojazdow/s), iterations
    to lista wektorow, gdzie kazdy wektor to reprezentacja drogi. Iterations sluzy do wizualizacji symulacji, flow
    sluzy do budowania diagramu fundamentalnego
    """

    # wyliczenie ile komorek modelu przypada na jedna komorka standardowego modelu NagelSch
    car_length = 7.5
    cell_multip = int(car_length/cell_length)

    vmax = vmax * cell_multip
    num_of_vehicles = d * N

    cells = np.zeros(N*cell_multip).astype(int)
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
        index = index * cell_multip
        cells[index] = vehicles_speeds[vehicles_speeds_index]
        for tail_index in range(1, cell_multip):
            cells[index-tail_index] = -2
        vehicles_speeds_index += 1

    # lista wszystkich iteracji
    # symulacja offline, najpierw wszystko
    # wyliczane, a na koncu wyswietlana wizualizacja
    iterations = []

    for x in range(0, num_of_iterations):
        # zwiekszanie predkosci
        cells[cells >= 0] = cells[cells >= 0] + 1
        cells[cells > vmax] = vmax

        # hamowanie
        for i in np.nonzero(cells >= 0)[0]:
            v = cells[i]
            for k in range(1, v + 1):
                if cells[(i + k) % (N*cell_multip)] != -1:
                    cells[i] = k - 1
                    break

        # losowe hamowanie
        for i in np.nonzero(cells > 0)[0]:
            if random.random() < p:
                cells[i] = cells[i] - 1

        # przemieszczanie
        for i in np.nonzero(cells > 0)[0]:
            v = cells[i]
            j = (i + v) % (N * cell_multip)

            # czysc stary ogon
            for tail_index in range(1, cell_multip):
                cells[i - tail_index] = -1
            cells[i] = -1

            cells[j] = v
            # ogon pojazdu
            for tail_index in range(1, cell_multip):
                cells[j - tail_index] = -2

        # dodanie drogi do listy iteracji
        iterations.append(np.copy(cells))

    # liczymy srednia predkosc z ostatniej iteracji
    average_velocity = np.sum(cells[cells >= 0]) / np.sum(cells >= 0) / cell_multip
    flow = d * average_velocity
    return flow, iterations

def model_visualisation():
    [flow, iterations] = nagel_sch(20, 0.8, 5, 0.5, 120)

    cells = iterations[0]
    print(np.sum(cells >= 0))
    cells = iterations[-1]
    print(np.sum(cells >= 0))


    #dp.image_visualisation(iterations)
    dp.offline_visualisation_one_lane(iterations[:])

def compare_various_lengths():
    density_arr = np.arange(0.05, 0.6, 0.01)
    flow_arr_1 = np.zeros(len(density_arr))
    flow_arr_2 = np.zeros(len(density_arr))
    flow_arr_3 = np.zeros(len(density_arr))
    flow_arr_4 = np.zeros(len(density_arr))

    x = 1
    for _ in range(x):
        # badamy model dla roznych gestosci ruchu
        for i in range(0, len(flow_arr_1)):
            [flow_1, iterations] = nagel_sch(1000, density_arr[i], 5, 7.5, 0.3)
            [flow_2, iterations] = nagel_sch(1000, density_arr[i], 5, 1, 0.3)
            [flow_3, iterations] = nagel_sch(1000, density_arr[i], 5, 7.5, 0.5)
            [flow_4, iterations] = nagel_sch(1000, density_arr[i], 5, 1, 0.5)
            flow_arr_1[i] += flow_1
            flow_arr_2[i] += flow_2
            flow_arr_3[i] += flow_3
            flow_arr_4[i] += flow_4

    flow_arr_1 = flow_arr_1 / x
    flow_arr_2 = flow_arr_2 / x
    flow_arr_3 = flow_arr_3 / x
    flow_arr_4 = flow_arr_4 / x

    comprasion.fundamental_diagram_comprasion(flow_arr_1, density_arr, "l = 7.5, p = 0.3")
    comprasion.fundamental_diagram_comprasion(flow_arr_2, density_arr, "l = 1, p = 0.3")
    comprasion.fundamental_diagram_comprasion(flow_arr_3, density_arr, "l = 7.5, p = 0.5")
    comprasion.fundamental_diagram_comprasion(flow_arr_4, density_arr, "l = 1, p = 0.5")

    plt.legend()
    plt.savefig("p_short.png")

################
# MAIN
################

def main():
    compare_various_lengths()
    # uncomment this if you want to preview
    # model visualisation in console
    # model_visualisation()



if __name__ == "__main__":
    main()
