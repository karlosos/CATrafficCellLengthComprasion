import rickert_asym
import numpy as np


def test_lane(lane):
    was_last_car = False
    for i in lane:
        if i==-2:
            was_last_car = True
        elif i==-1:
            was_last_car = False
            if was_last_car:
                raise NameError('We have orphaned car')
        elif i>-1:
            was_last_car = False


def count_cars(iteration):
    moving_cars = np.transpose(np.nonzero(iteration >= 0))
    return moving_cars.size


def main():
    [flow, iterations] = rickert_asym(1000, 0.8, 5, 0.5, 120)
    print(iterations[-2:][0])
    #dp.offline_visualisation_two_lanes(iterations[-3:])

    if count_cars(iterations[:][-1]) == count_cars(iterations[:][0]):
        print("All cars are")
    else:
        print(count_cars(iterations[:][-1]))
        print(count_cars(iterations[:][0]))

    for i in iterations[0][:]:
        test_lane(i)


if __name__ == "__main__":
    main()
