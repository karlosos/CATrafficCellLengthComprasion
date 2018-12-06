import numpy as np
import matplotlib.pyplot as plt

import rickert_asym
import rickert_sym

def fundamental_diagram_comprasion(flow_arr, density_arr, name):
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
    plt.plot(density_arr, flow_arr, 'o')
    # aproksymacja
    line, = plt.plot(xp, p(xp), '--', label=name)
    plt.ylabel('Flow [vehicles/s]')
    plt.xlabel('Density [vehicles/m]')

density_arr = np.arange(0.05, 0.45, 0.01)
flow_arr_1 = np.copy(density_arr)
flow_arr_2 = np.copy(density_arr)

# model 1
for i in range(0, len(flow_arr_1)):
    [flow, iterations] = rickert_asym.rickert_asym(5000, density_arr[i], 5, 7.5)
    flow_arr_1[i] = flow

# model 2
for i in range(0, len(flow_arr_2)):
    [flow, iterations] = rickert_sym.rickert_sym(5000, density_arr[i], 5, 7.5)
    flow_arr_2[i] = flow

fundamental_diagram_comprasion(flow_arr_1, density_arr, "Rickert asym")
fundamental_diagram_comprasion(flow_arr_2, density_arr, "Rickert sym")
plt.legend()
plt.show()
