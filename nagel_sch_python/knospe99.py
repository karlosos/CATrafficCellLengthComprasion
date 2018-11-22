#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Zmodyfikowana wersja modelu NagelSch z zmieniona iloscia komorek. Mozliwosc uruchomienia
modelu jako klasycznego modelu NagelSch.
"""

import numpy as np
import random
import time
from os import system, name
import matplotlib.pyplot as plt


def fundamental_diagram(flow_arr, density_arr):
    """
    Rysowanie diagramu fundamentalnego, czyli wykresu gestosci
    (ilosc pojazdow na drodze) do flow (ilosc pojazdow na sekunde)

    :param flow_arr: wektor zbadanych flow dla roznych gestosci
    :param density_arr: wektor badanych gestosci
    :return:
    """
    # aproksymacja funkcji wielomianem stopnia 7
    z = np.polyfit(density_arr, flow_arr, 7)
    p = np.poly1d(z)

    # wektor osi x (gestosci) dla ktorych aproksymujemy flow
    xp = np.arange(density_arr[0], density_arr[density_arr.size - 1], 0.001)

    # punkty pomiarowe
    plt.plot(density_arr, flow_arr, 'bo')
    # aproksymacja
    plt.plot(xp, p(xp), 'g--')
    plt.ylabel('Flow [vehicles/s]')
    plt.xlabel('Density [vehicles/m]')
    plt.show()


def offline_visualisation(iterations):
    """
    Wizualizacja offline na podstawie wymikow zapisanych w iterations

    :param iterations: lista wektorow, gdzie kazdy wektor reprezentuje
    stan drogi w jednostce czasu
    :return:
    """
    for i in iterations:
        road1 = ""
        for j in i[0]:
            if j == -1:
                road1 += "."
            elif j == -2:
                road1 += "▮"
            else:
                road1 += str(j)

        road2 = ""
        for j in i[1]:
            if j == -1:
                road2 += "."
            elif j == -2:
                road2 += "▮"
            else:
                road2 += str(j)
        clear()
        print(road1)
        print(road2)
        time.sleep(1)


def image_visualisation(iterations):
    """
    Wizualizacja symulacji w formie obrazka

    :param iterations: lista wektorow, gdzie kazdy wektor reprezentuje
    stan drogi w jednostce czasu
    :return:
    """
    num_of_iterations = len(iterations)
    N = len(iterations[0])
    a = np.zeros(shape=(num_of_iterations, N))
    for i in range(N):
        for j in range(num_of_iterations):
            a[j, i] = 0 if iterations[j][i] == -1 else 1

    # showing image
    plt.imshow(a, cmap="Greys", interpolation="nearest")
    plt.show()


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


def knospe(N, d, vmax, cell_multip=1, num_of_iterations=30):
    """
    Implementacja modelu nagel_sch

    :param N: dlugosc drogi
    :param d: gestosc (ile % pojazdow na drodze, np. 0.5 to polowa
    drogi zajeta przez pojazdy)
    :param vmax: predkosc maksymalna
    :param cell_multip: na ile komorek powinna byc podzielona jedna komorka z normalnego modelu
    :param num_of_iterations: ile iteracji symulacji (jednostek czasu)

    :return: (flow, iterations) - flow to wektor zbadanych przepustowosci drogi (pojazdow/s), iterations
    to lista wektorow, gdzie kazdy wektor to reprezentacja drogi. Iterations sluzy do wizualizacji symulacji, flow
    sluzy do budowania diagramu fundamentalnego
    """

    vmax = vmax * cell_multip
    num_of_vehicles = d * N

    cells = np.zeros((2, N*cell_multip)).astype(int)
    cells = cells - 1

    # lambda do znalezienia indeksow gdzie wstawic samochody
    # m to liczba elementow do wstawienia do macierzy
    # n to dlugosc wektora
    # zwraca indeksy wektora pod ktore nalezy wstawic elementy
    # aby mialy w miare jednakowe odstepy
    f = lambda m, n: [i * n // m + n // (2 * m) for i in range(m)]
    vehicles_indices = f(np.ceil(num_of_vehicles).astype(int), N)
    vehicles_speeds_lane_1 = np.random.randint(0, vmax, N)
    vehicles_speeds_lane_2 = np.random.randint(0, vmax, N)

    # wypelniamy droge losowymi samochodami (predkosciami)
    vehicles_speeds_index = 0
    for index in vehicles_indices:
        index = index * cell_multip
        cells[0][index] = vehicles_speeds_lane_1[vehicles_speeds_index]
        cells[1][index] = vehicles_speeds_lane_2[vehicles_speeds_index]
        for tail_index in range(1, cell_multip):
            cells[0][index-tail_index] = -2
            cells[1][index-tail_index] = -2
        vehicles_speeds_index += 1

    # lista wszystkich iteracji
    # symulacja offline, najpierw wszystko
    # wyliczane, a na koncu wyswietlana wizualizacja
    iterations = []
    iterations.append(np.copy(cells))

    for x in range(0, num_of_iterations):
        # zwiekszanie predkosci
        cells[:][cells >= 0] = cells[:][cells >= 0] + 1
        cells[:][cells > vmax] = vmax

        # pobierz indeksy pojazdow ktore maja predkosc wieksza niz 0
        # pierwszy element to indeks pasa
        # drugi element to indeks pojazdu na pasie
        moving_cars = np.transpose(np.nonzero(cells > 0))

        # hamowanie
        for i in moving_cars:
            lane_index = i[0]
            car_index = i[1]
            v = cells[lane_index][car_index]
            print("iteration: ", x, " index:", i, " v:", v)
            for k in range(1, v + 1):
                if cells[lane_index][(car_index + k) % (N*cell_multip)] != -1:
                    cells[lane_index][car_index] = k - 1
                    break

        # # losowe hamowanie
        moving_cars = np.transpose(np.nonzero(cells > 0))
        for i in moving_cars:
            if random.random() < 0.3:
                lane_index = i[0]
                car_index = i[1]
                cells[lane_index][car_index] = cells[lane_index][car_index] - 1

        moving_cars = np.transpose(np.nonzero(cells > 0))
        # przemieszczanie
        for i in moving_cars:
            lane_index = i[0]
            car_index = i[1]

            v = cells[lane_index][car_index]
            j = (car_index + v) % (N * cell_multip)

            # czysc stary ogon
            for tail_index in range(1, cell_multip):
                cells[lane_index][car_index - tail_index] = -1
            cells[lane_index][car_index] = -1

            cells[lane_index][j] = v
            # ogon pojazdu
            for tail_index in range(1, cell_multip):
                cells[lane_index][j - tail_index] = -2

        # dodanie drogi do listy iteracji
        iterations.append(np.copy(cells))

    # liczymy srednia predkosc z ostatniej iteracji
    average_velocity = np.sum(cells[cells >= 0]) / np.sum(cells >= 0) / cell_multip
    flow = d * average_velocity
    return flow, iterations


################
# MAIN
################


density_arr = np.arange(0.05, 0.6, 0.01)
flow_arr = np.copy(density_arr)

# # badamy model dla roznych gestosci ruchu
# for i in range(0, len(flow_arr)):
#     [flow, iterations] = nagel_sch(1000, density_arr[i], 5, 7)
#     flow_arr[i] = flow
#
# fundamental_diagram(flow_arr, density_arr)

[flow, iterations] = knospe(20, 0.8, 5, 5, 120)
#image_visualisation(iterations)
offline_visualisation(iterations)
