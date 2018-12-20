import numpy as np
import random
import data_presentation as dp


class Car:
    def __init__(self, road, y, x, length=7.5):
        self.v = 0
        self.v_next_step = 0
        self.v_max = 20
        self.x = x
        self.y = y  # lane index
        self.b = False
        self.b_next_step = False
        self.road = road

        self.p_d = 0.1
        self.p_b = 0.94
        self.p_0 = 0.05

        self.p = 0

        self.length = length
        self.length_in_cells = int(self.length / road.cell_length)

    def next_car(self):
        for i in range(self.road.N):
            if self.road.cells[self.y][(self.x + i + 1) % (self.road.N-1)] != -1:
                return self.road.cars[self.road.cells[self.y][(self.x + i + 1) % (self.road.N-1)]]

    def gap_to_next_car(self):
        c = self.next_car()
        if c.x > self.x:
            return c.x - c.length_in_cells - self.x
        elif c.x < self.x:
            return (self.road.N - self.x) + (c.x - c.length_in_cells)
        elif c.x == self.x:
            return self.road.N

    def calculate_breaking_probability(self):
        t_h = self.t_h()
        t_s = self.t_s()

        n_car = self.next_car()
        if n_car.b is True and t_h < t_s:
            return self.p_b
        elif self.v == 0 and (n_car.b is True and t_h < t_s) == False:
            return self.p_0
        else:
            return self.p_d

    def t_h(self):
        v = 1
        if (self.v > 0):
            v = self.v
        t_h = self.gap_to_next_car() / v
        return t_h

    def t_s(self):
        t_s = min(self.v, self.road.h)
        return t_s

    def v_anticipated(self):
        n_car = self.next_car()
        return min(n_car.gap_to_next_car(), n_car.v)

    def effective_distance(self):
        return self.gap_to_next_car() + max(self.v_anticipated() - self.road.gap_safety, 0)

class Road:
    def __init__(self, N, d, cell_length, num_of_iterations):
        self.N = N
        self.num_of_iterations = num_of_iterations
        self.d = d
        self.cell_length = cell_length
        #self.num_of_vehicles = d * N
        self.cells = np.zeros((2, N)).astype(int)
        self.cells = self.cells - 1

        self.h = 6
        self.gap_safety = 7

        self.cars = []

    def add_car(self, y, x, car_length = 7.5):
        c = Car(self, y, x, car_length)

        # check if can add car
        for i in range(c.length_in_cells):
            if self.cells[y][x-i] != -1:
                return None

        self.cars.append(c)
        index_of_car = len(self.cars) - 1

        for i in range(c.length_in_cells):
            self.cells[y][x-i] = index_of_car

        return c

    def step_0(self):
        for car in self.cars:
            car.p = car.calculate_breaking_probability()
            car.b_next_step = False

    def step_1(self):
        for car in self.cars:
            n_car = car.next_car()
            print(car.t_h(), car.t_s(), car.p)
            if (n_car.b == False and car.b == False) or (car.t_h() >= car.t_s()):
                car.v_next_step = min(car.v + 1, car.v_max)
                print("Acceleration: ", car.v_next_step)

    def step_2(self):
        for car in self.cars:
            car.v_next_step = min(car.effective_distance(), car.v)
            if car.v_next_step < car.v:
                car.b_next_step = True

    def step_3(self):
        for car in self.cars:
            p = car.calculate_breaking_probability()
            if random.random() < p:
                car.v_next_step = max(car.v_next_step - 1, 0)
                if p == car.p_b:
                    car.b_next_step = True

    def step_4(self):
        self.cells = np.zeros((2, self.N)).astype(int)
        self.cells = self.cells - 1

        for index_of_car, car in enumerate(self.cars):
            car.b = car.b_next_step
            car.v = car.v_next_step
            car.x = (car.x + car.v) % self.N

            for i in range(car.length_in_cells):
                self.cells[car.y][car.x - i] = index_of_car

    def simulation(self):
        self.populate_road()
        iterations = []
        iterations.append(self.iteration_visualisation())

        for i in range(self.num_of_iterations):
            print("It: ", i)
            self.step_0()
            self.step_1()
            self.step_2()
            self.step_3()
            self.step_4()
            iterations.append(self.iteration_visualisation())

        return iterations

    def populate_road(self):
        # lambda do znalezienia indeksow gdzie wstawic samochody
        # m to liczba elementow do wstawienia do macierzy
        # n to dlugosc wektora
        # zwraca indeksy wektora pod ktore nalezy wstawic elementy
        # aby mialy w miare jednakowe odstepy
        f = lambda m, n: [i * n // m + n // (2 * m) for i in range(m)]
        vehicles_indices = f(np.ceil(self.d * self.N).astype(int), self.N-1)

        for x in vehicles_indices:
            self.add_car(0, x)

        self.fill_road()

    def fill_road(self):
        for index_of_car, car in enumerate(self.cars):
            for i in range(car.length_in_cells):
                self.cells[car.y][car.x - i] = index_of_car

    def iteration_visualisation(self):
        cells = np.zeros((2, self.N)).astype(int)
        cells = cells - 1

        for index_of_car, car in enumerate(self.cars):
            for i in range(car.length_in_cells):
                cells[car.y][car.x - i] = car.v

        return np.copy(cells)


def main():
    s = Road(500, 0.1, 1.5, 300)
    sim = s.simulation()
    dp.offline_visualisation_two_lanes(sim)

if __name__ == "__main__":
    main()