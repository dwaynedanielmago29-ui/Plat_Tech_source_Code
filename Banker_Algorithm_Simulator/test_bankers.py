import unittest

from Bankers import (
    validate_algorithm_inputs,
    calculate_need,
    calculate_available,
    safety_algorithm,
    run_bankers_algorithm,
)


class TestValidateAlgorithmInputs(unittest.TestCase):

    def setUp(self):
        self.total = [10, 5, 7]
        self.allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ]
        self.maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]

    def test_valid_inputs_return_process_and_resource_counts(self):
        result = validate_algorithm_inputs(
            self.total, self.allocation, self.maximum
        )
        self.assertEqual(result, (5, 3))

    def test_empty_total_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_algorithm_inputs([], self.allocation, self.maximum)

    def test_empty_allocation_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_algorithm_inputs(self.total, [], self.maximum)

    def test_empty_maximum_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_algorithm_inputs(self.total, self.allocation, [])

    def test_different_process_counts_are_rejected(self):
        with self.assertRaises(ValueError):
            validate_algorithm_inputs(
                self.total, self.allocation, self.maximum[:-1]
            )

    def test_wrong_number_of_resource_values_is_rejected(self):
        bad_allocation = [row[:] for row in self.allocation]
        bad_allocation[0] = [0, 1]

        with self.assertRaises(ValueError):
            validate_algorithm_inputs(
                self.total, bad_allocation, self.maximum
            )

    def test_negative_resource_value_is_rejected(self):
        bad_total = [10, -5, 7]

        with self.assertRaises(ValueError):
            validate_algorithm_inputs(
                bad_total, self.allocation, self.maximum
            )

    def test_non_integer_resource_value_is_rejected(self):
        bad_total = [10, 5.0, 7]

        with self.assertRaises(ValueError):
            validate_algorithm_inputs(
                bad_total, self.allocation, self.maximum
            )

    def test_boolean_resource_value_is_rejected(self):
        bad_total = [10, True, 7]

        with self.assertRaises(ValueError):
            validate_algorithm_inputs(
                bad_total, self.allocation, self.maximum
            )

    def test_allocation_cannot_exceed_maximum(self):
        bad_allocation = [row[:] for row in self.allocation]
        bad_allocation[0][0] = 8

        with self.assertRaises(ValueError):
            validate_algorithm_inputs(
                self.total, bad_allocation, self.maximum
            )

    def test_allocated_resources_cannot_exceed_total(self):
        small_total = [5, 5, 7]

        with self.assertRaises(ValueError):
            validate_algorithm_inputs(
                small_total, self.allocation, self.maximum
            )


class TestBankersCalculations(unittest.TestCase):

    def setUp(self):
        self.total = [10, 5, 7]
        self.allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ]
        self.maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]

    def test_calculate_need_returns_expected_matrix(self):
        expected_need = [
            [7, 4, 3],
            [1, 2, 2],
            [6, 0, 0],
            [0, 1, 1],
            [4, 3, 1],
        ]

        result = calculate_need(self.allocation, self.maximum)

        self.assertEqual(result, expected_need)

    def test_calculate_available_returns_expected_vector(self):
        result = calculate_available(self.total, self.allocation)

        self.assertEqual(result, [3, 3, 2])


class TestSafetyAlgorithm(unittest.TestCase):

    def test_safe_system_returns_expected_safe_sequence(self):
        available = [3, 3, 2]
        allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ]
        need = [
            [7, 4, 3],
            [1, 2, 2],
            [6, 0, 0],
            [0, 1, 1],
            [4, 3, 1],
        ]

        result = safety_algorithm(available, allocation, need)

        self.assertTrue(result["safe"])
        self.assertEqual(
            result["safe_sequence"],
            ["P1", "P3", "P0", "P2", "P4"],
        )
        self.assertEqual(result["finish"], [True, True, True, True, True])
        self.assertEqual(result["final_work"], [10, 5, 7])

    def test_unsafe_system_returns_no_safe_sequence(self):
        available = [0]
        allocation = [[1], [0]]
        need = [[1], [1]]

        result = safety_algorithm(available, allocation, need)

        self.assertFalse(result["safe"])
        self.assertEqual(result["safe_sequence"], [])
        self.assertEqual(result["finish"], [False, False])
        self.assertEqual(result["final_work"], [0])

    def test_partially_executable_unsafe_system_is_reported_unsafe(self):
        available = [0]
        allocation = [[1], [0]]
        need = [[0], [2]]

        result = safety_algorithm(available, allocation, need)

        self.assertFalse(result["safe"])
        self.assertEqual(result["safe_sequence"], ["P0"])
        self.assertEqual(result["finish"], [True, False])
        self.assertEqual(result["final_work"], [1])

    def test_trace_contains_initialization_checks_execution_and_final_event(self):
        available = [1]
        allocation = [[1]]
        need = [[1]]

        result = safety_algorithm(available, allocation, need)
        events = [entry["event"] for entry in result["trace"]]

        self.assertEqual(events[0], "INITIALIZATION")
        self.assertIn("CHECK", events)
        self.assertIn("EXECUTE", events)
        self.assertEqual(events[-1], "FINAL")

    def test_final_trace_event_matches_result(self):
        available = [1]
        allocation = [[1]]
        need = [[1]]

        result = safety_algorithm(available, allocation, need)
        final_event = result["trace"][-1]

        self.assertEqual(final_event["safe"], result["safe"])
        self.assertEqual(final_event["sequence"], result["safe_sequence"])
        self.assertEqual(final_event["work"], result["final_work"])
        self.assertEqual(final_event["finish"], result["finish"])


class TestRunBankersAlgorithm(unittest.TestCase):

    def setUp(self):
        self.total = [10, 5, 7]
        self.allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2],
        ]
        self.maximum = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3],
        ]

    def test_main_function_returns_expected_results(self):
        result = run_bankers_algorithm(
            self.total, self.allocation, self.maximum
        )

        self.assertEqual(result["process_count"], 5)
        self.assertEqual(result["resource_count"], 3)
        self.assertEqual(result["total"], self.total)
        self.assertEqual(result["allocation"], self.allocation)
        self.assertEqual(result["maximum"], self.maximum)
        self.assertEqual(result["available"], [3, 3, 2])
        self.assertEqual(
            result["need"],
            [
                [7, 4, 3],
                [1, 2, 2],
                [6, 0, 0],
                [0, 1, 1],
                [4, 3, 1],
            ],
        )
        self.assertTrue(result["safe"])
        self.assertEqual(
            result["safe_sequence"],
            ["P1", "P3", "P0", "P2", "P4"],
        )
        self.assertEqual(result["finish"], [True, True, True, True, True])
        self.assertIn("trace", result)
        self.assertEqual(result["final_work"], [10, 5, 7])

    def test_main_function_rejects_invalid_input(self):
        invalid_total = [5, 5, 7]

        with self.assertRaises(ValueError):
            run_bankers_algorithm(
                invalid_total, self.allocation, self.maximum
            )

    def test_input_matrices_are_not_modified(self):
        total_before = self.total[:]
        allocation_before = [row[:] for row in self.allocation]
        maximum_before = [row[:] for row in self.maximum]

        run_bankers_algorithm(self.total, self.allocation, self.maximum)

        self.assertEqual(self.total, total_before)
        self.assertEqual(self.allocation, allocation_before)
        self.assertEqual(self.maximum, maximum_before)


if __name__ == "__main__":
    unittest.main(verbosity=2)
