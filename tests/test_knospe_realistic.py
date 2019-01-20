import unittest
import knospe_realistic as knsp
import numpy as np


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

    def test_incentive_criterion_BrakeLightsAreOn_ReturnFalse(self):
        self.c.b = True
        self.assertEqual(self.c.incentive_criterion(), False)

    def test_incentive_criterion_VelocityIsGreaterThanDistance_ReturnTrue(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 0)
        c2 = self.r.add_car(0, 20, 2)
        c2.v = 9

        c1.v = c1.gap_to_next_car() + 3
        c1.b = False

        self.assertEqual(c1.incentive_criterion(), True)

    def test_incentive_criterion_VelocityIsLesserThanDistance_ReturnFalse(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 0)
        c2 = self.r.add_car(0, 20, 2)
        c2.v = 9

        c1.v = c1.gap_to_next_car() - 3
        c1.b = False

        self.assertEqual(c1.incentive_criterion(), False)

    def test_incentive_criterion_VelocityIsEqualToDistance_ReturnFalse(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 0)
        c2 = self.r.add_car(0, 20, 2)
        c2.v = 9

        c1.v = c1.gap_to_next_car()
        c1.b = False

        self.assertEqual(c1.incentive_criterion(), False)


class TestCarOtherLaneMethods(unittest.TestCase):
    def setUp(self):
        self.r = knsp.Road(100, 0.1, 1, 100)

    def test_pred_car_other_lane_TwoCarsOnOtherLaneTwoInSomeDistanceFromCar_ReturnNextCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)
        succ = self.r.add_car(1, 0)
        pred = self.r.add_car(1, 30)

        self.assertEqual(pred, c1.pred_car_other_lane())

    def test_succ_car_other_lane_TwoCarsOnOtherLaneTwoInSomeDistanceFromCar_ReturnPreviousCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)
        succ = self.r.add_car(1, 0)
        pred = self.r.add_car(1, 30)

        self.assertEqual(succ, c1.succ_car_other_lane())

    def test_pred_car_other_lane_TwoCarsOnOtherLaneOccupyingCarSpace_ReturnNextCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)
        succ = self.r.add_car(1, 15)
        pred = self.r.add_car(1, 25)

        #print(self.r.cells[0])
        #print(self.r.cells[1])
        #print("Pred: ", pred.x)
        #print("Calculated pred: ", c1.pred_car_other_lane().x)

        self.assertEqual(pred, c1.pred_car_other_lane())

    def test_succ_car_other_lane_TwoCarsOnOtherLaneOccupyingCarSpace_ReturnPreviousCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)
        succ = self.r.add_car(1, 15)
        pred = self.r.add_car(1, 25)

        self.assertEqual(pred, c1.succ_car_other_lane())

    def test_succ_car_other_lane_OneCarOtherLane_ReturnPreviousCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)
        #succ = self.r.add_car(1, 15)
        pred = self.r.add_car(1, 25)

        self.assertEqual(pred, c1.succ_car_other_lane())

    def test_succ_car_other_lane_OneCarOtherLane_ReturnNextCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)
        succ = self.r.add_car(1, 15)
        #pred = self.r.add_car(1, 25)

        self.assertEqual(succ, c1.pred_car_other_lane())

    def test_pred_car_other_lane_TwoCarsOnOtherLaneOneOccupySameSpace_ReturnNextCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)
        succ = self.r.add_car(1, 20)
        pred = self.r.add_car(1, 30)

        self.assertEqual(pred, c1.pred_car_other_lane())

    def test_succ_car_other_lane_TwoCarsOnOtherLaneOneOccupySameSpace_ReturnPreviousCar(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)
        succ = self.r.add_car(1, 20)
        pred = self.r.add_car(1, 30)

        self.assertEqual(succ, c1.succ_car_other_lane())


class TestCarTailMethods(unittest.TestCase):
    def test_tail_x_CarInMiddleOfRoad_return_position_of_car_end(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 20)

        self.assertEqual(c1.tail_x(), 14)

    def test_tail_x_CarInStartAndEndOfRoad_return_position_of_car_end(self):
        self.r = knsp.Road(100, 0.1, 1, 100)
        c1 = self.r.add_car(0, 5)

        self.assertEqual(c1.tail_x(), 99)

    def test_tail_x_CarOfLength1InMiddleOfRoad_return_position_of_car_end(self):
        self.r = knsp.Road(100, 0.1, 7, 100)
        c1 = self.r.add_car(0, 20)

        self.assertEqual(c1.tail_x(), 20)

    def test_tail_x_CarOfLength1InStartAndEndOfRoad_return_position_of_car_end(self):
        self.r = knsp.Road(100, 0.1, 7, 100)
        c1 = self.r.add_car(0, 5)

        self.assertEqual(c1.tail_x(), 5)

    def test_calculate_distance(self):
        self.r = knsp.Road(12, 0.1, 7, 100)
        c1 = self.r.add_car(0, 5)
        self.assertEqual(c1.calculate_distance(3, 7), 3)
        self.assertEqual(c1.calculate_distance(7, 3), 7)

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

class TestPopulateMethod(unittest.TestCase):
    def test_simulation_increasingNumberOfCarLength1(self):
        density_arr = np.arange(0.05, 0.6, 0.01)
        flow_arr = np.zeros(len(density_arr))

        previous_number = 0
        # badamy model dla roznych gestosci ruchu
        for i in range(0, len(density_arr)):
            s = knsp.Road(50, density_arr[i], 1, 50)
            s.simulation()
            print("Gestosc teoretyczna vs realna: ", s.d, np.sum(s.cells > -1)/(s.N * 2))
            self.assertGreaterEqual(len(s.cars), previous_number)
            previous_number = len(s.cars)

    def test_populate_increasingNumberOfCarLength7(self):
        density_arr = np.arange(0.05, 0.6, 0.01)
        flow_arr = np.zeros(len(density_arr))

        previous_number = 0
        # badamy model dla roznych gestosci ruchu
        for i in range(0, len(density_arr)):
            s = knsp.Road(50, density_arr[i], 7, 50)
            s.populate_road()
            self.assertGreaterEqual(len(s.cars), previous_number)
            previous_number = len(s.cars)

    def test_populate_increasingNumberOfCarLength(self):
        density_arr = np.arange(0.05, 0.6, 0.01)
        flow_arr = np.zeros(len(density_arr))

        previous_number = 0
        # badamy model dla roznych gestosci ruchu
        for i in range(0, len(density_arr)):
            s = knsp.Road(50, density_arr[i], 1, 50)
            s.populate_road()
            print(s.d, s.N, len(s.cars), previous_number)
            self.assertGreaterEqual(len(s.cars), previous_number)
            previous_number = len(s.cars)

    def test_vehicleIndices_increasingNumberOfCarLength(self):
        density_arr = np.arange(0.05, 0.6, 0.01)
        s = knsp.Road(50, 0.1, 1, 50)
        flow_arr = np.zeros(len(density_arr))

        previous_number = 0
        # badamy model dla roznych gestosci ruchu
        for i in range(0, len(density_arr)):
            vehicles_indeces = s.get_vehicle_indeces_for_populate(density_arr[i], 350)
            self.assertGreaterEqual(len(vehicles_indeces), previous_number)
            previous_number = len(vehicles_indeces)

if __name__ == '__main__':
    unittest.main()