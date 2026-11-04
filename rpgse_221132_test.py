# pyright: reportPrivateUsage=false

from collections import Counter
import unittest
from rpgse_221132 import RollSimulator

class TestRpgSE221132(unittest.TestCase):

    def _do_bumps(self, dice_roll_counts: Counter[int], threshold: int, num_bumps: int):
        test_msg: str = f"Test operation - bump +{num_bumps}:\n    {sorted(dice_roll_counts.items())}"
        rs: RollSimulator = RollSimulator(dice_roll_counts.total(), threshold, num_bumps)
        rs._bump_dice_counts(dice_roll_counts, num_bumps)
        test_msg += f"\n    to\n    {sorted(dice_roll_counts.items())}"
        print(test_msg)

    def _do_drops(self, dice_roll_counts: Counter[int], threshold: int, num_drops: int):
        test_msg: str = f"Test operation - drop -{num_drops}:\n    {sorted(dice_roll_counts.items())}"
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


if __name__ == '__main__':
    unittest.main()