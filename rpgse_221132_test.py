# pyright: reportPrivateUsage=false

from collections import Counter
import unittest
from rpgse_221132 import RollSimulator

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


if __name__ == '__main__':
    unittest.main()