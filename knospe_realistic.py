import numpy as np
import random
import data_presentation as dp


class Car:
    def __init__(self, road, y, x, length=7.5):
        self.v = 15
        self.v_next_step = 15
        self.v_max = 20 * road.cell_multip
        self.x = x
        self.y = y  # lane index
        self.y_next_step = y
        self.b = False
        self.b_next_step = False
        self.road = road

        self.p_d = 0.1
        self.p_b = 0.94
        self.p_0 = 0.5

        self.p = 0

        self.length = length
        self.length_in_cells = int(self.length / road.cell_length)

    def next_car(self):
        for i in range(self.road.N):
            if self.road.cells[self.y][(self.x + i + 1) % (self.road.N-1)] != -1:
                return self.road.cars[self.road.cells[self.y][(self.x + i + 1) % (self.road.N-1)]]

    def gap_to_next_car(self):
        """
        Calculates d - distance-headway, gap to the next car
        :return: d
        """
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
        elif self.v == 0 and (n_car.b is True and t_h < t_s) is False:
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

    def incentive_criterion(self):
        return self.b == 0 and self.v > self.gap_to_next_car()

    def other_lane(self):
        if self.y == 0:
            other_lane = 1
        else:
            other_lane = 0

        return other_lane

    def pred_car_other_lane(self):
        """
        Next car on other lane
        :return:
        """
        other_lane = self.other_lane()

        for i in range(self.road.N):
            if self.road.cells[other_lane][(self.x + i + 1) % (self.road.N-1)] != -1:
                return self.road.cars[self.road.cells[other_lane][(self.x + i + 1) % (self.road.N-1)]]

    def succ_car_other_lane(self):
        """
        Previous car on other lane
        :return:
        """
        other_lane = self.other_lane()

        for i in range(self.road.N):
            if self.road.cells[other_lane][(self.x - (i + 1)) % (self.road.N-1)] != -1:
                return self.road.cars[self.road.cells[other_lane][(self.x - (i + 1)) % (self.road.N-1)]]

    def tail_x(self):
        return (self.x - self.length_in_cells + 1) % self.road.N

    def calculate_distance(self, x1, x2):
        if (x1 < x2):
            return (x2 - x1 - 1) % self.road.N
        elif (x1 > x2):
            return self.road.N - (x1 - x2 - 1) - 2
        else:
            return 0

    def d_succ(self):
        succ = self.succ_car_other_lane()
        return self.calculate_distance(succ.x, self.x)

    def d_pred(self):
        pred = self.pred_car_other_lane()
        return self.calculate_distance(self.x, pred.x)

    def effective_distance_pred(self):
        pred = self.pred_car_other_lane()
        d_pred = self.d_pred()
        v_anti = min(pred.gap_to_next_car(), pred.v)
        return d_pred + max(v_anti - self.road.gap_safety, 0)

    def safety_criterion(self):
        return self.effective_distance_pred() >= self.v and self.d_succ() >= self.succ_car_other_lane().v

    def change_lane(self):
        self.y_next_step = self.other_lane()

class Road:
    def __init__(self, N, d, cell_length, num_of_iterations):
        self.num_of_iterations = num_of_iterations
        self.d = d
        self.cell_length = cell_length
        self.cell_multip = int(7.5/cell_length)
        self.N = N * self.cell_multip
        #self.num_of_vehicles = d * N
        self.cells = np.zeros((2, self.N)).astype(int)
        self.cells = self.cells - 1

        self.h = 6
        self.gap_safety = 7

        self.cars = []

    def add_car(self, y, x, car_length = 7.5):
        c = Car(self, y, x, car_length)

        # check if can add car
        for i in range(c.length_in_cells):
            if self.cells[y][x-i] != -1:
                print("Couldn't add car!")
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
            if (n_car.b == False and car.b == False) or (car.t_h() >= car.t_s()):
                car.v_next_step = min(car.v + 1, car.v_max)

    def step_2(self):
        for car in self.cars:
            car.v_next_step = min(car.effective_distance(), car.v_next_step)
            if car.v_next_step < car.v:
                car.b_next_step = True

    def step_3(self):
        for car in self.cars:
            if random.random() < car.p:
                car.v_next_step = max(car.v_next_step - 1, 0)
                if car.p == car.p_b:
                    car.b_next_step = True

    def step_4(self):
        self.cells = np.zeros((2, self.N)).astype(int)
        self.cells = self.cells - 1

        for index_of_car, car in enumerate(self.cars):

            car.b = car.b_next_step
            car.v = car.v_next_step

            car.b_next_step = False

            car.x = (car.x + car.v) % self.N

            for i in range(car.length_in_cells):
                self.cells[car.y][car.x - i] = index_of_car

    def simulation(self):
        self.populate_road()
        iterations = []
        iterations.append(self.iteration_visualisation())

        for i in range(self.num_of_iterations):
            self.change_lanes()
            self.step_0()
            self.step_1()
            self.step_2()
            self.step_3()
            self.step_4()
            iterations.append(self.iteration_visualisation())

        # liczymy srednia predkosc z ostatniej iteracji
        average_velocity = 0
        for car in self.cars:
            average_velocity += car.v

        average_velocity = average_velocity/len(self.cars)

        flow = self.d * average_velocity

        return flow, iterations

    def change_lanes(self):
        for car in self.cars:
            car.y_next_step = car.y
            if car.incentive_criterion() and car.safety_criterion():
                car.change_lane()

        for car in self.cars:
            car.y = car.y_next_step

    def get_vehicle_indeces_for_populate(self, d, n):
        # lambda do znalezienia indeksow gdzie wstawic samochody
        # m to liczba elementow do wstawienia do macierzy
        # n to dlugosc wektora
        # zwraca indeksy wektora pod ktore nalezy wstawic elementy
        # aby mialy w miare jednakowe odstepy
        f = lambda m, n: [i * n // m + n // (2 * m) for i in range(m)]
        return f(np.ceil(d * n).astype(int), n - 1)

    def populate_road(self):
        vehicles_indices = self.get_vehicle_indeces_for_populate(self.d, self.N)

        for x in vehicles_indices:
            self.add_car(0, x)

        for x in vehicles_indices:
            self.add_car(1, x)

        self.cars[0].v_max = 5

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


def simulation():
    s = Road(500, 0.05, 1, 300)
    flow, iterations = s.simulation()
    dp.offline_visualisation_two_lanes(iterations)


def fundamental_diagram():
    density_arr = np.arange(0.05, 0.6, 0.01)
    flow_arr = np.zeros(len(density_arr))

    cell_length = 7

    cell_multip = Road(10, 0.5, cell_length, 50).cell_multip
    number_of_retries = 5
    for j in range(number_of_retries):
        #badamy model dla roznych gestosci ruchu
        for i in range(0, len(density_arr)):
            s = Road(100, density_arr[i]/cell_multip, cell_length, 50)
            [flow, iterations] = s.simulation()
            flow_arr[i] += flow
            print(i/len(density_arr), len(s.cars), s.d)


    # for i in range(number_of_retries):
    #     flow_arr[i] = flow_arr[i]/(number_of_retries+1)

    dp.fundamental_diagram(flow_arr/(number_of_retries+1), density_arr)

def main():
    fundamental_diagram()


if __name__ == "__main__":
    main()
