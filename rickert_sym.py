#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Model rickert symetryczny
"""

import numpy as np
import random
import comprasion
import matplotlib.pyplot as plt
import rickert_asym as ra

import data_presentation as dp

def rickert_sym(N, d, vmax, cell_length, p, p_change, num_of_iterations=30):
    """
    Implementacja modelu rickert symetryczny

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

    cells = np.zeros((2, N*cell_multip)).astype(int)
    cells = cells - 1

    # parametry do rickert
    l_other_back = vmax + 1
    #p_change = 1

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
        # zmienianie pasow (ruch poprzeczny)

        # patrz do przodu czy ktos jest przed toba
        # zobacz na drugim pasie czy tam jest lepiej
        # zobacz w tyl na drugim pasie czy komus nie zajedziesz drogi
        # pobierz indeksy pojazdow ktore maja predkosc wieksza niz 0
        # pierwszy element to indeks pasa
        # drugi element to indeks pojazdu na pasie
        moving_cars = np.transpose(np.nonzero(cells >= 0))
        # kopia drogi - aby zapewnic rownoleglosc fazy zmiany pasow
        cells_copy = np.zeros((2, N*cell_multip)).astype(int)
        cells_copy = cells_copy - 1

        for i in moving_cars:
            lane_index = i[0]
            car_index = i[1]

            v = cells[lane_index][car_index]
            l = v+1
            l_other = l

            # flaga okreslajaca czy pojazd zmienil pas
            has_changed_lane = False

            # sprawdz czy jakis samochod bedzie blokowac
            is_someone_ahead = False
            for k in range(1, l):
                if cells[lane_index][(car_index + k) % (N * cell_multip)] != -1:
                    is_someone_ahead = True
                    break

            if is_someone_ahead:
                # sprawdz czy na drugim pasie ktos bedzie blokowac
                is_someone_ahead_other_lane = False
                lane_index_other = 1 if lane_index == 0 else 0
                for k in range(0, l_other):
                    if cells[lane_index_other][(car_index + k) % (N * cell_multip)] != -1:
                        is_someone_ahead_other_lane = True
                        break

                if not is_someone_ahead_other_lane:
                    # czy zajedziemy komus droge
                    is_someone_before_other_lane = False
                    for k in range(1, l_other_back):
                        if cells[lane_index_other][(car_index - k) % (N * cell_multip)] != -1:
                            is_someone_before_other_lane = True
                            break

                    if not is_someone_before_other_lane:
                        # czy zmienic pas (losowosc)
                        if random.random() < p_change:
                            # print("Zmiana pasa, wooohoooo!")
                            # zmiana pasa - przeniesienie pojazdu z jednego pasu na drugi

                            # # czysc stary pas
                            # for tail_index in range(1, cell_multip):
                            #     cells[lane_index][car_index - tail_index] = -1
                            # cells[lane_index][car_index] = -1

                            # nowy pas
                            if cells[lane_index_other][car_index] == -1:
                                has_changed_lane = True
                                cells_copy[lane_index_other][car_index] = v

                                # ogon pojazdu
                                for tail_index in range(1, cell_multip):
                                    cells_copy[lane_index_other][car_index - tail_index] = -2


            # jezeli nie zmienil pasu to skopiuj w to samo miejsce
            if has_changed_lane == False:
                cells_copy[lane_index][car_index] = v

                for tail_index in range(1, cell_multip):
                    cells_copy[lane_index][car_index - tail_index] = -2

        cells = cells_copy.copy()

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
            #print("iteration: ", x, " index:", i, " v:", v)
            for k in range(1, v + 1):
                if cells[lane_index][(car_index + k) % (N*cell_multip)] != -1:
                    cells[lane_index][car_index] = k-1
                    break

        # # losowe hamowanie
        moving_cars = np.transpose(np.nonzero(cells > 0))
        for i in moving_cars:
            if random.random() < p:
                lane_index = i[0]
                car_index = i[1]
                cells[lane_index][car_index] = cells[lane_index][car_index] - 1

        cells_copy = np.zeros((2, N*cell_multip)).astype(int)
        cells_copy = cells_copy - 1

        moving_cars = np.transpose(np.nonzero(cells >= 0))
        # przemieszczanie
        for i in moving_cars:
            lane_index = i[0]
            car_index = i[1]

            v = cells[lane_index][car_index]
            j = (car_index + v) % (N * cell_multip)

            # czysc stary ogon
            # for tail_index in range(1, cell_multip):
            #     cells[lane_index][car_index - tail_index] = -1
            # cells[lane_index][car_index] = -1

            cells_copy[lane_index][j] = v
            # ogon pojazdu
            for tail_index in range(1, cell_multip):
                cells_copy[lane_index][j - tail_index] = -2

        cells = cells_copy

        # dodanie drogi do listy iteracji
        iterations.append(np.copy(cells))

    # liczymy srednia predkosc z ostatniej iteracji
    average_velocity = np.sum(cells[cells >= 0]) / np.sum(cells >= 0) / cell_multip
    flow = d * average_velocity
    return flow, iterations

def compare():
    density_arr = np.arange(0.05, 0.6, 0.01)
    flow_arr_1 = np.zeros(len(density_arr))
    flow_arr_2 = np.zeros(len(density_arr))
    flow_arr_3 = np.zeros(len(density_arr))
    flow_arr_4 = np.zeros(len(density_arr))

    x = 50
    for _ in range(x):
        # badamy model dla roznych gestosci ruchu
        for i in range(0, len(flow_arr_1)):
            [flow_1, iterations] = rickert_sym(N=1000, d=density_arr[i], vmax=5, cell_length=7.5, p=0.2, p_change=1)
            [flow_2, iterations] = rickert_sym(N=1000, d=density_arr[i], vmax=5, cell_length=0.5, p=0.2, p_change=1)
            [flow_3, iterations] = ra.rickert_asym(N=1000, d=density_arr[i], vmax=5, cell_length=7.5, p=0.2, p_change=1)
            [flow_4, iterations] = ra.rickert_asym(N=1000, d=density_arr[i], vmax=5, cell_length=0.5, p=0.2, p_change=1)
            flow_arr_1[i] += flow_1
            flow_arr_2[i] += flow_2
            flow_arr_3[i] += flow_3
            flow_arr_4[i] += flow_4

    flow_arr_1 = flow_arr_1 / x
    flow_arr_2 = flow_arr_2 / x
    flow_arr_3 = flow_arr_3 / x
    flow_arr_4 = flow_arr_4 / x

    comprasion.fundamental_diagram_comprasion(flow_arr_1, density_arr, "sym l = 7.5")
    comprasion.fundamental_diagram_comprasion(flow_arr_2, density_arr, "sym l = 0.5")
    comprasion.fundamental_diagram_comprasion(flow_arr_3, density_arr, "asym l = 7.5")
    comprasion.fundamental_diagram_comprasion(flow_arr_4, density_arr, "asym l = 0.5")

    plt.legend()
    plt.savefig("rickert_sym_vs_asym.png")

################
# MAIN
################


def main():
    compare()

if __name__ == "__main__":
    main()
