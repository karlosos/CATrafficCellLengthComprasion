#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
            a[j, i] = 1 if iterations[j][i] > -1 else 0

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
    treshhold_probability = 0.2
    p_curr = [1 if probability > treshhold_probability else 0 for probability in np.random.rand(cells.shape[0])]
    p_prev = [1 for el in p_curr]
    flow_sum = 0
    for x in range(0, num_of_iterations):
        # zwiekszanie predkosci
        for idx in range(len(cells)):
            if cells[idx] == 0:
                if p_curr[idx] or not p_prev[idx]:
                    cells[idx] += 1
        cells[cells > 0] = cells[cells > 0] + 1
        cells[cells > vmax] = vmax
        p_prev = p_curr
        p_curr = [1 if probability > treshhold_probability else 0 for probability in np.random.rand(cells.shape[0])]

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

        average_velocity = np.sum(cells[cells >= 0]) / np.sum(cells >= 0)
        flow_sum += d * average_velocity

    # liczymy sredni flow ze wszystkich iteracji (w calym czasie symulacji)
    average_flow = flow_sum / num_of_iterations
    return average_flow, iterations


################
# MAIN
################


density_arr = np.arange(0.05, 0.6, 0.01)
flow_arr = np.copy(density_arr)

# badamy model dla roznych gestosci ruchu
for i in range(0, len(flow_arr)):
    [flow, iterations] = nagel_sch(10000, density_arr[i], 5)
    flow_arr[i] = flow

fundamental_diagram(flow_arr, density_arr)

[flow, iterations] = nagel_sch(80, 0.3, 5, 120)
# image_visualisation(iterations)
offline_visualisation(iterations)