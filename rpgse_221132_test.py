# pyright: reportPrivateUsage=false

from collections import Counter
from decimal import Decimal
from math import pow
from rpgse_221132 import DIE_SIZE, get_printable_results, RollSimulator
import unittest

class TestRpgSE221132(unittest.TestCase):

    #
    # BUMPS & DROPS
    #

    def _do_bumps(self, dice_roll_counts: Counter[int], threshold: int, num_bumps: int):
        test_msg: str = f"Test operation - bump {num_bumps}:\n    {sorted(dice_roll_counts.items())}"
        rs: RollSimulator = RollSimulator(dice_roll_counts.total(), threshold, num_bumps)
        rs._bump_dice_counts(dice_roll_counts, num_bumps)
        test_msg += f"\n    to\n    {sorted(dice_roll_counts.items())}"
        print(test_msg)

    def _do_drops(self, dice_roll_counts: Counter[int], threshold: int, num_drops: int):
        test_msg: str = f"Test operation - drop {num_drops}:\n    {sorted(dice_roll_counts.items())}"
        rs: RollSimulator = RollSimulator(dice_roll_counts.total(), threshold, -1 * num_drops)
        rs._drop_dice_counts(dice_roll_counts, num_drops)
        test_msg += f"\n    to\n    {sorted(dice_roll_counts.items())}"
        print(test_msg)

    def test_bumps_01(self):
        # input rolls: [2, 3, 5]
        roll_counts: Counter[int] = Counter({1:0, 2:1, 3:1, 4:0, 5:1, 6:0})
        threshold: int = 4
        num_bumps: int = 1
        self._do_bumps(roll_counts, threshold, num_bumps)
        # expected result: [2, 4, 5]
        expected_result = Counter({1:0, 2:1, 3:0, 4:1, 5:1, 6:0})
        self.assertDictEqual(expected_result, roll_counts)

    def test_bumps_02(self):
        # input rolls: [2, 3, 5]
        roll_counts: Counter[int] = Counter({1:0, 2:1, 3:1, 4:0, 5:1, 6:0})
        threshold: int = 4
        num_bumps: int = 2
        self._do_bumps(roll_counts, threshold, num_bumps)
        # expected result: [2, 4, 6]
        expected_result = Counter({1:0, 2:1, 3:0, 4:1, 5:0, 6:1})
        self.assertDictEqual(expected_result, roll_counts)

    def test_bumps_03(self):
        # input rolls: [2, 3, 5]
        roll_counts: Counter[int] = Counter({1:0, 2:1, 3:1, 4:0, 5:1, 6:0})
        threshold: int = 4
        num_bumps: int = 3
        self._do_bumps(roll_counts, threshold, num_bumps)
        # expected result: [4, 4, 5]
        expected_result = Counter({1:0, 2:0, 3:0, 4:2, 5:1, 6:0})
        self.assertDictEqual(expected_result, roll_counts)

    def test_bumps_04(self):
        # input rolls: [2, 3, 5]
        roll_counts: Counter[int] = Counter({1:0, 2:1, 3:1, 4:0, 5:1, 6:0})
        threshold: int = 4
        num_bumps: int = 4
        self._do_bumps(roll_counts, threshold, num_bumps)
        # expected result: [4, 4, 6]
        expected_result = Counter({1:0, 2:0, 3:0, 4:2, 5:0, 6:1})
        self.assertDictEqual(expected_result, roll_counts)

    def test_bumps_05(self):
        # input rolls: [2, 3, 5]
        roll_counts: Counter[int] = Counter({1:0, 2:1, 3:1, 4:0, 5:1, 6:0})
        threshold: int = 4
        num_bumps: int = 5
        self._do_bumps(roll_counts, threshold, num_bumps)
        # expected result: [4, 4, 6]
        expected_result = Counter({1:0, 2:0, 3:0, 4:2, 5:0, 6:1})
        self.assertDictEqual(expected_result, roll_counts)

    def test_bumps_06(self):
        # input rolls: [2, 3, 5]
        roll_counts: Counter[int] = Counter({1:0, 2:1, 3:1, 4:0, 5:1, 6:0})
        threshold: int = 4
        num_bumps: int = 6
        self._do_bumps(roll_counts, threshold, num_bumps)
        # expected result: [4, 6, 6]
        expected_result = Counter({1:0, 2:0, 3:0, 4:1, 5:0, 6:2})
        self.assertDictEqual(expected_result, roll_counts)

    def test_bumps_nowhere_to_go(self):
        # input rolls: [6, 6, 6]
        roll_counts: Counter[int] = Counter({1:0, 2:0, 3:0, 4:0, 5:0, 6:3})
        threshold: int = 4
        num_bumps: int = 3
        self._do_bumps(roll_counts, threshold, num_bumps)
        # expected result: [6, 6, 6] (i.e. no change)
        expected_result = Counter({1:0, 2:0, 3:0, 4:0, 5:0, 6:3})
        self.assertDictEqual(expected_result, roll_counts)

    def test_drops_01(self):
        # input rolls: [4, 5, 6]
        roll_counts: Counter[int] = Counter({1:0, 2:0, 3:0, 4:1, 5:1, 6:1})
        threshold: int = 4
        num_drops: int = 1
        self._do_drops(roll_counts, threshold, num_drops)
        # expected result: [3, 5, 6]
        expected_result = Counter({1:0, 2:0, 3:1, 4:0, 5:1, 6:1})
        self.assertDictEqual(expected_result, roll_counts)

    def test_drops_02(self):
        # input rolls: [4, 5, 6]
        roll_counts: Counter[int] = Counter({1:0, 2:0, 3:0, 4:1, 5:1, 6:1})
        threshold: int = 4
        num_drops: int = 2
        self._do_drops(roll_counts, threshold, num_drops)
        # expected result: [3, 5, 5]
        expected_result = Counter({1:0, 2:0, 3:1, 4:0, 5:2, 6:0})
        self.assertDictEqual(expected_result, roll_counts)

    def test_drops_03(self):
        # input rolls: [4, 5, 6]
        roll_counts: Counter[int] = Counter({1:0, 2:0, 3:0, 4:1, 5:1, 6:1})
        threshold: int = 4
        num_drops: int = 3
        self._do_drops(roll_counts, threshold, num_drops)
        # expected result: [3, 3, 6]
        expected_result = Counter({1:0, 2:0, 3:2, 4:0, 5:0, 6:1})
        self.assertDictEqual(expected_result, roll_counts)

    def test_drops_04(self):
        # input rolls: [4, 5, 6]
        roll_counts: Counter[int] = Counter({1:0, 2:0, 3:0, 4:1, 5:1, 6:1})
        threshold: int = 4
        num_drops: int = 4
        self._do_drops(roll_counts, threshold, num_drops)
        # expected result: [3, 3, 5]
        expected_result = Counter({1:0, 2:0, 3:2, 4:0, 5:1, 6:0})
        self.assertDictEqual(expected_result, roll_counts)

    def test_drops_05(self):
        # input rolls: [4, 5, 6]
        roll_counts: Counter[int] = Counter({1:0, 2:0, 3:0, 4:1, 5:1, 6:1})
        threshold: int = 4
        num_drops: int = 5
        self._do_drops(roll_counts, threshold, num_drops)
        # expected result: [3, 3, 5] (with 1 unused drop)
        expected_result = Counter({1:0, 2:0, 3:2, 4:0, 5:1, 6:0})
        self.assertDictEqual(expected_result, roll_counts)

    def test_drops_06(self):
        # input rolls: [4, 5, 6]
        roll_counts: Counter[int] = Counter({1:0, 2:0, 3:0, 4:1, 5:1, 6:1})
        threshold: int = 4
        num_drops: int = 6
        self._do_drops(roll_counts, threshold, num_drops)
        # expected result: [3, 3, 3]
        expected_result = Counter({1:0, 2:0, 3:3, 4:0, 5:0, 6:0})
        self.assertDictEqual(expected_result, roll_counts)

    def test_drops_nowhere_to_go(self):
        # input rolls: [1, 1, 1]
        roll_counts: Counter[int] = Counter({1:3, 2:0, 3:0, 4:0, 5:0, 6:0})
        threshold: int = 4
        num_drops: int = 3
        self._do_drops(roll_counts, threshold, num_drops)
        # expected result: [1, 1, 1] (i.e. no change)
        expected_result = Counter({1:3, 2:0, 3:0, 4:0, 5:0, 6:0})
        self.assertDictEqual(expected_result, roll_counts)

    #
    # ROLLS <-> ROLL COUNTS
    #

    def test_convert_rolls_to_roll_counts_basic(self):
        rolls: list[int] = [1,2,3,4,5,6]
        expected: Counter[int] = Counter({1:1, 2:1, 3:1, 4:1, 5:1, 6:1})
        rs: RollSimulator = RollSimulator(0,0,0)
        actual: Counter[int] = rs._convert_rolls_to_dice_histo_counts(rolls)
        self.assertDictEqual(expected, actual)

    def test_convert_rolls_to_roll_counts_irregular(self):
        rolls: list[int] = [5,2,5,3,3,5]
        expected: Counter[int] = Counter({1:0, 2:1, 3:2, 4:0, 5:3, 6:0})
        rs: RollSimulator = RollSimulator(0,0,0)
        actual: Counter[int] = rs._convert_rolls_to_dice_histo_counts(rolls)
        self.assertDictEqual(expected, actual)

    def test_convert_rolls_to_roll_counts_empty(self):
        rolls: list[int] = []
        expected: Counter[int] = Counter({1:0, 2:0, 3:0, 4:0, 5:0, 6:0})
        rs: RollSimulator = RollSimulator(0,0,0)
        actual: Counter[int] = rs._convert_rolls_to_dice_histo_counts(rolls)
        self.assertDictEqual(expected, actual)

    def test_convert_roll_counts_to_rolls_basic(self):
        roll_counts: Counter[int] = Counter({1:1, 2:1, 3:1, 4:1, 5:1, 6:1})
        expected: tuple[int, ...] = (1,2,3,4,5,6)
        rs: RollSimulator = RollSimulator(0,0,0)
        actual: tuple[int, ...] = rs._convert_dice_histo_counts_to_rolls(roll_counts)
        self.assertSequenceEqual(expected, actual)

    def test_convert_roll_counts_to_rolls_irregular(self):
        roll_counts: Counter[int] = Counter({5:3, 1:0, 3:2, 2:1, 4:0, 6:0})
        expected: tuple[int, ...] = (2,3,3,5,5,5)
        rs: RollSimulator = RollSimulator(0,0,0)
        actual: tuple[int, ...] = rs._convert_dice_histo_counts_to_rolls(roll_counts)
        self.assertSequenceEqual(expected, actual)

    def test_convert_roll_counts_to_rolls_empty(self):
        roll_counts: Counter[int] = Counter({1:0, 2:0, 3:0, 4:0, 5:0, 6:0})
        expected: tuple[int, ...] = ()
        rs: RollSimulator = RollSimulator(0,0,0)
        actual: tuple[int, ...] = rs._convert_dice_histo_counts_to_rolls(roll_counts)
        self.assertSequenceEqual(expected, actual)

    #
    # OVERALL FUNCTIONALITY
    #
    
    def test_two_dice_with_one_bump(self):
        '''
        21 unique roll outcomes (6 doubles, 30/2=15 unique non-doubles).
        Pre-drop, doubles have 1/36 odds and non-doubles have 2/36 odds.
        Selected threshold is 4.

        Before bump, odds of (# successes, sixes) are expected to be:
          (0, 0): 9/36 (3/36: [1,1], [2,2], [3,3] ; 6/36: [1,2], [1,3], [2,3])
          (0, 1): 0 [impossible]
          (0, 2): 0 [impossible]
          (1, 0): 12/36 ([1,5], [2,5], [3,5], [1,4], [2,4], [3,4])
          (1, 1): 6/36 ([1,6], [2,6], [3,6])
          (1, 2): 0 [impossible]
          (2, 0): 4/36 (2/36: [4,4], [5,5]; 1/18: [4,5])
          (2, 1): 4/36 ([4,6], [5,6])
          (2, 2): 1/36 ([6,6])

        One bump should have the following effects:
          (0,0) -> (1,0): 5/36
            [1,3] -> [1,4], [2,3] -> [2,4], [3,3] -> [3,4]
          (1,0) -> (2,0): 4/36
            [3,4] -> [4,4], [3,5] -> [4,5]
          (1,1) -> (2,1): 2/36
            [3,6] -> [4,6]
          (1,0) -> (1,1): 4/36
            [1,5] -> [1,6], [2,5] -> [2,6]
          (2,0) -> (2,1): 3/36
            [4,5] -> [4,6], [5,5] -> [5,6]
          (2,1) -> (2,2): 2/36
            [5,6] -> [6,6]

        So the final odds should be:
          (0, 0): 9/36 - 5/36 = 4/36 (0.1111)
          (0, 1): 0 [impossible]
          (0, 2): 0 [impossible]
          (1, 0): 12/36 + 5/36 - 4/36 - 4/36 = 9/36 (0.25)
          (1, 1): 6/36 - 2/36 + 4/36 = 8/36 (0.2222)
          (1, 2): 0 [impossible]
          (2, 0): 4/36 + 4/36 - 3/36 = 5/36 (0.1389)
          (2, 1): 4/36 + 2/36 + 3/36 - 2/36 = 7/36 (0.1944)
          (2, 2): 1/36 + 2/36 = 3/36 (0.0833)
        '''
        roll_mod: int = 1
        expected_counts: Counter[tuple[int, int]] = Counter(
                {(0,0): 4, (1,0): 9, (1,1): 8, (2,0): 5, (2,1): 7, (2,2): 3})
        self._test_two_dice_with_roll_mod(roll_mod, expected_counts)

    def test_two_dice_with_one_drop(self):
        '''
        21 unique roll outcomes (6 doubles, 30/2=15 unique non-doubles).
        Pre-drop, doubles have 1/36 odds and non-doubles have 2/36 odds.
        Selected threshold is 4.

        Before bump, odds of (# successes, sixes) are expected to be:
          (0, 0): 9/36 (3/36: [1,1], [2,2], [3,3] ; 3/18: [1,2], [1,3], [2,3])
          (0, 1): 0 [impossible]
          (0, 2): 0 [impossible]
          (1, 0): 12/36 ([1,5], [2,5], [3,5], [1,4], [2,4], [3,4])
          (1, 1): 6/36 ([1,6], [2,6], [3,6])
          (1, 2): 0 [impossible]
          (2, 0): 4/36 (2/36: [4,4], [5,5]; 1/18: [4,5])
          (2, 1): 4/36 ([4,6], [5,6])
          (2, 2): 1/36 ([6,6])

        One drop should have the following effects:
          (2,2) -> (2,1): 1/36
            [6,6] -> [5,6]
          (2,1) -> (2,0): 2/36
            [5,6] -> [5,5]
          (2,1) -> (1,1): 2/36
            [4,6] -> [3,6]
          (2,0) -> (1,0): 3/36
            [4,5] -> [3,5], [4,4] -> [3,4]
          (1,1) -> (1,0): 6/36
            [3,6] -> [3,5], [2,6] -> [2,5], [1,6] -> [1,5]
          (1,0) -> (0,0): 6/36
            [3,4] -> [3,3], [2,4] -> [2,3], [1,4] -> [1,3]

        So the final odds should be:
          (0, 0): 9/36 + 6/36 = 15/36
          (0, 1): 0 [impossible]
          (0, 2): 0 [impossible]
          (1, 0): 12/36 + 3/36 + 6/36 - 6/36 = 15/36
          (1, 1): 6/36 + 2/36 - 6/36 = 2/36
          (1, 2): 0 [impossible]
          (2, 0): 4/36 + 2/36 - 3/36 = 3/36
          (2, 1): 4/36 + 1/36 - 2/36 - 2/36 = 1/36
          (2, 2): 1/36 - 1/36 = 0
        '''
        roll_mod: int = -1
        expected_counts: Counter[tuple[int, int]] = Counter({
                (0,0): 15, (1,0): 15, (1,1): 2, (2,0): 3, (2,1): 1})
        self._test_two_dice_with_roll_mod(roll_mod, expected_counts)

    def _test_two_dice_with_roll_mod(self, roll_mod: int, expected_counts: Counter[tuple[int, int]]):
        num_dice: int = 2
        threshold: int = 4
        expected_percent_strings: list[str] = \
                self._stringify_expected_counts_as_percents(expected_counts, num_dice)

        rs: RollSimulator = RollSimulator(num_dice, threshold, roll_mod)
        actual_counts: Counter[tuple[int, ...]] = rs.get_summarized_results()
        self.assertDictEqual(expected_counts, actual_counts)
        actual_percent_strings: list[str] = \
                [line.lstrip() for line in get_printable_results(rs, False)[1:]]
        self.assertSequenceEqual(expected_percent_strings, actual_percent_strings)

    def _stringify_expected_counts_as_percents(self,
                                               expected_counts: Counter[tuple[int, int]],
                                               num_dice: int) -> list[str]:
        denominator: int = int(pow(DIE_SIZE, num_dice))
        expected_percents: dict[tuple[int, int], Decimal] = \
                {k: ((Decimal(v) / Decimal(denominator)) * Decimal(100))
                 for k, v in expected_counts.items()}
        return [f'{k}: {v:.3}%' for k, v in expected_percents.items()]


if __name__ == '__main__':
    unittest.main()