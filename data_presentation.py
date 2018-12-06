import numpy as np
import time
import matplotlib.pyplot as plt
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

def offline_visualisation_two_lanes(iterations):
    """
    Wizualizacja offline na podstawie wymikow zapisanych w iterations

    Dotyczy wizualizacji modeli o dwoch pasach

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

def offline_visualisation_one_lane(iterations):
    """
    Wizualizacja offline na podstawie wymikow zapisanych w iterations

    Dotyczy wizualizacji modeli jednopasmowych

    :param iterations: lista wektorow, gdzie kazdy wektor reprezentuje
    stan drogi w jednostce czasu
    :return:
    """
    for i in iterations:
        road = ""
        for j in i:
            if j == -1:
                road += "."
            elif j == -2:
                road += "▮"
            else:
                road += str(j)
        clear()
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
            a[j, i] = 0 if iterations[j][i] == -1 else 1

    # showing image
    plt.imshow(a, cmap="Greys", interpolation="nearest")
    plt.show()
