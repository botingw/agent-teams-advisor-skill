"""Tests for dice_roller.py"""

import pytest
from dice_roller import roll_dice, calculate_total


class TestRollDice:
    """Tests for the roll_dice function."""

    def test_default_returns_one_result(self):
        results = roll_dice()
        assert len(results) == 1

    def test_returns_correct_number_of_dice(self):
        for n in [1, 2, 5, 10]:
            results = roll_dice(num_dice=n)
            assert len(results) == n

    def test_default_faces_in_range(self):
        for _ in range(100):
            results = roll_dice()
            assert all(1 <= r <= 6 for r in results)

    def test_custom_faces_in_range(self):
        for num_faces in [4, 8, 10, 12, 20, 100]:
            for _ in range(50):
                results = roll_dice(num_dice=3, num_faces=num_faces)
                assert all(1 <= r <= num_faces for r in results)

    def test_single_face_die(self):
        results = roll_dice(num_dice=5, num_faces=1)
        assert results == [1, 1, 1, 1, 1]

    def test_zero_dice_returns_empty(self):
        results = roll_dice(num_dice=0)
        assert results == []

    def test_results_are_integers(self):
        results = roll_dice(num_dice=3, num_faces=6)
        assert all(isinstance(r, int) for r in results)

    def test_negative_dice_raises_error(self):
        with pytest.raises(ValueError):
            roll_dice(num_dice=-1)

    def test_zero_faces_raises_error(self):
        with pytest.raises(ValueError):
            roll_dice(num_faces=0)

    def test_negative_faces_raises_error(self):
        with pytest.raises(ValueError):
            roll_dice(num_faces=-1)

    def test_large_number_of_dice(self):
        results = roll_dice(num_dice=1000, num_faces=6)
        assert len(results) == 1000
        assert all(1 <= r <= 6 for r in results)


class TestCalculateTotal:
    """Tests for the calculate_total function."""

    def test_single_value(self):
        assert calculate_total([5]) == 5

    def test_multiple_values(self):
        assert calculate_total([1, 2, 3, 4, 5]) == 15

    def test_empty_list(self):
        assert calculate_total([]) == 0

    def test_all_ones(self):
        assert calculate_total([1, 1, 1]) == 3

    def test_all_sixes(self):
        assert calculate_total([6, 6, 6]) == 18

    def test_matches_roll_dice_output(self):
        results = roll_dice(num_dice=5, num_faces=6)
        assert calculate_total(results) == sum(results)


class TestIntegration:
    """Integration tests combining roll_dice and calculate_total."""

    def test_total_within_expected_range(self):
        num_dice, num_faces = 3, 6
        results = roll_dice(num_dice=num_dice, num_faces=num_faces)
        total = calculate_total(results)
        assert num_dice <= total <= num_dice * num_faces

    def test_single_die_total_equals_result(self):
        results = roll_dice(num_dice=1, num_faces=20)
        assert calculate_total(results) == results[0]

    def test_zero_dice_total_is_zero(self):
        results = roll_dice(num_dice=0)
        assert calculate_total(results) == 0
