import unittest
import knospe_realistic as knsp


class TestCarMethods(unittest.TestCase):
    def setUp(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        self.c = self.r.add_car(0, 0)

    def test_Constructor_CreatingDefaultCar_BrakeLightsAreOff(self):
        self.assertEqual(self.c.b, False)

    def test_Constructor_CreatingDefaultCarWithRoadCellLength1m_LengthInCellsEqual7(self):
        self.assertEqual(self.c.length_in_cells, 7)

    def test_v_anticipated_DIsLesser_ReturnGapOfNextVehicle(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 0)
        c1.v = 8
        c2 = self.r.add_car(0, 7, 2)
        c2.v = 7
        c3 = self.r.add_car(0, 12, 2)
        c3.v = 0

        print(self.r.cells)

        self.assertEqual(c1.v_anticipated(), 3)

    def test_v_anticipated_VIsLesser_ReturnGapOfNextVehicle(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 0)
        c1.v = 8
        c2 = self.r.add_car(0, 7, 2)
        c2.v = 1
        c3 = self.r.add_car(0, 12, 2)
        c3.v = 0

        print(self.r.cells)

        self.assertEqual(c1.v_anticipated(), 1)

    def test_v_anticipated_DIsGreater_ReturnGapOfNextVehicle(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 0)
        c1.v = 8
        c2 = self.r.add_car(0, 7, 2)
        c2.v = 7
        c3 = self.r.add_car(0, 40, 2)
        c3.v = 0

        print(self.r.cells)

        self.assertEqual(c1.v_anticipated(), 7)

    def test_effective_distance_VAntiIsLesserThanGapSafety_ReturnGap(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 0)
        c1.v = 8
        c2 = self.r.add_car(0, 7, 2)
        c2.v = 7
        c3 = self.r.add_car(0, 12, 2)
        c3.v = 0

        print(self.r.cells)

        self.assertEqual(c1.effective_distance(), 5)

    def test_effective_distance_VAntiIsBiggerThanGapSafety_ReturnGap(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 0)
        c1.v = 8
        c2 = self.r.add_car(0, 7, 2)
        c2.v = 9
        c3 = self.r.add_car(0, 40, 2)
        c3.v = 0

        print(self.r.cells)

        self.assertEqual(c1.effective_distance(), 7)

class TestCarMethodsNextCarHomogeneous(unittest.TestCase):
    def setUp(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        self.c = self.r.add_car(0, 0)

    def test_next_car_CreatingNewCarInFrontOfOldCar_ReturnNewCar(self):
        c2 = self.r.add_car(0, 10)
        c2_from_function = self.c.next_car()
        self.assertEqual(c2, c2_from_function)

    def test_next_car_CreatingNewCarBeforeOfOldCar_ReturnNewCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c2 = self.r.add_car(0, 30)
        c3 = self.r.add_car(0, 10)
        self.assertEqual(c3, c2.next_car())

    def test_next_car_CreatingNewCarInFrontOfOldCarNoDistance_ReturnNewCar(self):
        c2 = self.r.add_car(0, 7)
        c2_from_function = self.c.next_car()
        self.assertEqual(c2, c2_from_function)

    def test_gap_to_next_car_CarInFrontOf5Cells_Return5(self):
        c2 = self.r.add_car(0, 12)
        print(0, self.r.cars[0].x, self.r.cars[1].x)
        self.assertEqual(self.c.gap_to_next_car(), 5)

    def test_gap_to_next_car_CarInFrontOfNoDistance_Return0(self):
        c2 = self.r.add_car(0, 7)
        self.assertEqual(self.c.gap_to_next_car(), 0)

    def test_gap_to_next_car_CarBefore5Cells_Return73(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 30)
        c2 = self.r.add_car(0, 10)
        print(self.r.cells)
        self.assertEqual(c1.gap_to_next_car(), 73)

    def test_gap_to_next_car_CarBefore3Cells_Return76(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 30)
        c2 = self.r.add_car(0, 13)
        print(self.r.cells)
        self.assertEqual(c1.gap_to_next_car(), 76)

    def test_gap_to_next_car_OneCarOnLane_ReturnN(self):
        self.assertEqual(self.c.gap_to_next_car(), self.r.N)

class TestCarMethodsNextCarUnhomogeneous(unittest.TestCase):
    def setUp(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        self.c = self.r.add_car(0, 0, 5)

    def test_next_car_CreatingNewCarInFrontOfOldCar_ReturnNewCar(self):
        c2 = self.r.add_car(0, 10, 2)
        c2_from_function = self.c.next_car()
        self.assertEqual(c2, c2_from_function)

    def test_next_car_CreatingNewCarBeforeOfOldCar_ReturnNewCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c2 = self.r.add_car(0, 30, 6)
        c3 = self.r.add_car(0, 10, 2)
        self.assertEqual(c3, c2.next_car())

    def test_next_car_CreatingNewCarInFrontOfOldCarNoDistance_ReturnNewCar(self):
        c2 = self.r.add_car(0, 7, 1)
        c2_from_function = self.c.next_car()
        self.assertEqual(c2, c2_from_function)

    def test_gap_to_next_car_CarInFrontOf5Cells_Return10(self):
        c2 = self.r.add_car(0, 12, 2)
        print(self.r.cells)
        self.assertEqual(self.c.gap_to_next_car(), 10)

    def test_gap_to_next_car_CarInFrontOfNoDistance_Return0(self):
        c2 = self.r.add_car(0, 1, 1)
        print(self.r.cells)
        self.assertEqual(self.c.gap_to_next_car(), 0)

    def test_gap_to_next_car_CarBefore5Cells_Return70(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 30, 3)
        c2 = self.r.add_car(0, 10, 10)
        print(self.r.cells)
        self.assertEqual(c1.gap_to_next_car(), 70)

    def test_gap_to_next_car_CarBefore3Cells_Return73(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 30, 3)
        c2 = self.r.add_car(0, 13, 10)
        print(self.r.cells)
        self.assertEqual(c1.gap_to_next_car(), 73)

    def test_gap_to_next_car_OneCarOnLane_ReturnN(self):
        self.assertEqual(self.c.gap_to_next_car(), self.r.N)

class TestRoadMethods(unittest.TestCase):
    def setUp(self):
        self.r = knsp.Road(100, 0.1, 1, 100)

    def test_add_car_AddingCar_CarsHaveReferenceToTheSameRoad(self):
        c1 = self.r.add_car(0, 5)
        c2 = self.r.add_car(0, 15)

        self.assertEqual(c1.road, c2.road)
        self.assertEqual(len(self.r.cars), 2)

    def test_add_car_AddingCarsOneAfterOther_CarsWereAddedToRoad(self):
        c1 = self.r.add_car(0, 0)
        c2 = self.r.add_car(0, 7)

        self.assertEqual(c1.road, c2.road)
        self.assertEqual(len(self.r.cars), 2)

    def test_add_car_AddingCarCarOverlapDifferentCarOnHead_ReturnsNone(self):
        self.r.add_car(0, 10)
        c2 = self.r.add_car(0, 5)

        self.assertEqual(c2, None)
        self.assertEqual(len(self.r.cars), 1)

    def test_add_car_AddingCarCarOverlapDifferentCarOnTail_ReturnsNone(self):
        self.r.add_car(0, 5)
        c2 = self.r.add_car(0, 10)

        self.assertEqual(c2, None)
        self.assertEqual(len(self.r.cars), 1)

    def test_add_car_AddingCarCarOverlapOneCellDifferentCarOnTail_ReturnsNone(self):
        self.r.add_car(0, 0)
        c2 = self.r.add_car(0, 6)

        self.assertEqual(c2, None)
        self.assertEqual(len(self.r.cars), 1)



if __name__ == '__main__':
    unittest.main()