import numpy as np
import matplotlib.pyplot as plt

import knospe99
import nagel_sch_m

def fundamental_diagram(flow_arr, density_arr, name):
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
    plt.plot(xp, p(xp), '--')
    plt.ylabel('Flow [vehicles/s]')
    plt.xlabel('Density [vehicles/m]')

density_arr = np.arange(0.05, 0.6, 0.01)
flow_arr_knospe = np.copy(density_arr)
flow_arr_nagel = np.copy(density_arr)

# knospe
for i in range(0, len(flow_arr_knospe)):
    [flow, iterations] = knospe99.knospe(1000, density_arr[i], 5, 7)
    flow_arr_knospe[i] = flow

# nagel
for i in range(0, len(flow_arr_nagel)):
    [flow, iterations] = knospe99.knospe(1000, density_arr[i], 5, 1)
    flow_arr_nagel[i] = flow

fundamental_diagram(flow_arr_nagel, density_arr, "Nagel")
fundamental_diagram(flow_arr_knospe, density_arr, "Nagel 7")
plt.show()
