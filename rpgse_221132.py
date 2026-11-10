import argparse
from collections import Counter
from decimal import Decimal
from itertools import product
from math import comb
import sys
from textwrap import indent
from typing import Any, Sequence

DIE_SIZE: int = 6
INDENT = '    '
ROLL_BLOCK_SIZE = 1_000_000

class RollSimulator(object):
    """Rolls dice, applies bumps/drops, and counts the results."""

    def __init__(self, dice_per_roll: int, threshold: int, roll_mod: int):
        self._raw_roll_counts: Counter[tuple[int, ...]] = Counter()
        self._modded_roll_counts: Counter[tuple[int, ...]] = Counter()
        self._dice_per_roll = dice_per_roll
        self._threshold = threshold
        self._roll_mod = roll_mod

        
    def _stringify_counter_as_percents(self, counter: Counter[Any]) -> list[str]:
        lines: list[str] = []
        k: Any
        for k in sorted(counter):
            fraction: Decimal = Decimal(counter[k]) / Decimal(counter.total())
            lines.append(f'{k}: {fraction * 100:.3}%')
        return lines

    
    def _count_results_by_successes_and_maxes(self) -> Counter[tuple[int, int]]:
        """
        Converts the known roll outcomes into (# of successes, # of max-values)
        tuples, and then counts the numbers of each. 
        """
        successes_and_maxes_counts: Counter[tuple[int, int]] = Counter()
        k: tuple[int, ...]
        v: int
        for k, v in self._modded_roll_counts.items():
            num_successes: int = 0
            num_maxes: int = 0
            die: int
            for die in k:
                if (die >= self._threshold):
                    num_successes += 1
                if (die == DIE_SIZE):
                    num_maxes += 1
            successes_and_maxes_counts[(num_successes, num_maxes)] += v
        return successes_and_maxes_counts

        
    def get_printable_result(self, include_roll_details: bool=False) -> list[str]:
        lines: list[str] = []
        
        # Results by successes + maxes
        lines.append(f'Final roll odds grouped by (# successes, # {DIE_SIZE}s):')
        summary_lines = (indent(s, INDENT)
                         for s
                         in self._stringify_counter_as_percents(
                             self._count_results_by_successes_and_maxes()))
        lines.extend(summary_lines)
        
        # Results by roll
        if (include_roll_details):
            # Expectation is calculated with the "multichoose" formula.
            num_possible_raw_rolls: int = comb(
                    DIE_SIZE + self._dice_per_roll - 1, self._dice_per_roll)
            lines.append(f'Expected {num_possible_raw_rolls} possible roll '
                    + 'outcomes (before bumps & drops).')
            lines.append('Actual number of raw rolls logged: '
                    + f'{len(self._raw_roll_counts)}')
            
            lines.append('Roll odds for raw / unmodified rolls:')
            raw_detail_lines = (indent(s, INDENT)
                                for s
                                in self._stringify_counter_as_percents(
                                        self._raw_roll_counts))
            lines.extend(raw_detail_lines)
            
            lines.append('Roll odds for final / modified / bumped-and-dropped rolls:')
            modded_detail_lines = (indent(s, INDENT)
                            for s
                            in self._stringify_counter_as_percents(
                                self._modded_roll_counts))
            lines.extend(modded_detail_lines)
        
        return lines

    def _convert_rolls_to_dice_histo_counts(self, rolls: Sequence[int]) -> Counter[int]:
        """
        E.g. converts (1, 2, 5, 5, 6) or [1, 2, 5, 5, 6] to
        Counter({1: 1, 2: 1, 3: 0, 4: 0, 5: 2, 6: 1})
        """
        dice_counts: Counter[int] = Counter({k: 0 for k in range(1, DIE_SIZE + 1)})
        single_roll_value: int
        for single_roll_value in rolls:
            dice_counts[single_roll_value] += 1
        return dice_counts

    def _convert_dice_histo_counts_to_rolls(self, dice_counts: Counter[int]) -> tuple[int, ...]:
        """
        E.g. converts Counter({1: 1, 2: 1, 3: 0, 4: 0, 5: 2, 6: 1})
        to (1, 2, 5, 5, 6)
        """
        rolls: list[int] = list(dice_counts.elements())
        rolls.sort()
        return tuple(rolls)

    def _bump_dice_counts(self, dice_counts: Counter[int], num_bumps: int):
        """
        Mutates the input dice_counts Counter according to the number of bumps
        """
        bumps_remaining: int = num_bumps
        # Maximize successes first, go for max-rolls second
        target: int
        for target in (self._threshold, DIE_SIZE):
            # For each target,
            # do all "useful" single-bumps, then double-bumps, then triple, etc.
            bump_distance: int
            for bump_distance in range(1, DIE_SIZE - 1):
                source: int = target - bump_distance
                if source < 1:
                    continue
                while dice_counts[source] > 0 and (
                        bumps_remaining - bump_distance >= 0):
                    dice_counts[source] -= 1
                    dice_counts[target] += 1
                    bumps_remaining -= bump_distance

    def _drop_dice_counts(self, dice_counts: Counter[int], num_drops: int):
        """
        Mutates the input dice_counts Counter according to the number of drops
        """
        drops_remaining: int = num_drops
        # Minimize successes first, then try to undo undo max-rolls second.
        target: int
        for target in (self._threshold - 1, DIE_SIZE - 1):
            # For each target,
            # do all "useful" single-drops, then double-drops, then triple, etc.
            drop_distance: int
            for drop_distance in range(1, DIE_SIZE - 1):
                source: int = target + drop_distance
                if source > DIE_SIZE:
                    continue
                while dice_counts[source] > 0 and (
                        drops_remaining - drop_distance >= 0):
                    dice_counts[source] -= 1
                    dice_counts[target] += 1
                    drops_remaining -= drop_distance
    
    def _bump_and_drop_rolls(self, raw_rolls: tuple[int, ...]) -> tuple[int, ...]:
        if (self._roll_mod == 0):
            return raw_rolls
        else:
            dice_counts: Counter[int] = self._convert_rolls_to_dice_histo_counts(
                    list(raw_rolls))
            if (self._roll_mod > 0):
                self._bump_dice_counts(dice_counts, self._roll_mod)
            else: # < 0
                self._drop_dice_counts(dice_counts, abs(self._roll_mod))
            return self._convert_dice_histo_counts_to_rolls(dice_counts)
    
    def compute_roll_odds(self):
        # Count, proportionally, the odds of each raw roll combination.
        # For example, with three dice, 
        # we represent the odds of rolling-three-1s as ==1,
        # and the odds of rolling-two-1s-and-a-2 as ==3,
        # because there are three distinct ways to roll the latter.
        # ((1,1,2), (1,2,1), (2,1,1))
        for roll in product(range(1, DIE_SIZE + 1), repeat=self._dice_per_roll):
            self._raw_roll_counts[tuple(sorted(roll))] += 1
    
        # Then apply bumps and drops.
        # This might lead to collisions, so we total the odds accordingly.
        k: tuple[int, ...]
        v: int
        for k, v in self._raw_roll_counts.items():
            modded_roll: tuple[int, ...] = self._bump_and_drop_rolls(k)
            self._modded_roll_counts[modded_roll] += v


def getBooleanUserInput(question: str) -> bool:
    while True:
        response: str = input(question + " [Y/N] ")
        if (response == 'Y' or response == 'y'):
            return True
        elif (response == 'N' or response == 'n'):
            return False

def main():
    parser = argparse.ArgumentParser(
                    prog='rpgse_221132',
                    description='Computes odds of rolls under the bump/drop system described in https://rpg.stackexchange.com/q/221132/.')
    parser.add_argument('-n', '--num-dice', type=int, required=True,
                        help='The number of d6 dice to roll (>=1).')
    parser.add_argument('-t', '--threshold', type=int, required=True,
                        help='Number that a die must equal or exceed to count as a success.')
    parser.add_argument('-b', '--bumps', type=int, default=0,
                        help='The number of "bumps" (plus-ones) to apply to dice after the roll.')
    parser.add_argument('-d', '--drops', type=int, default=0,
                            help='The number of "drops" (minus-ones) to apply to dice after the roll.')
    parser.add_argument('--print-roll-details', action='store_true',
                            help='Print chance of each distinct roll. (This may be very long.)')
    args = parser.parse_args()
    
    # Input validation
    # Error states
    if (args.num_dice < 1):
        print('ERROR! Number of dice cannot be less than 1.', file=sys.stderr)
        exit(1)
    if (args.bumps < 0 or args.drops < 0):
        print('ERROR! Bumps and/or drops cannot be negative numbers.', file=sys.stderr)
        exit(2)
    # Warning states
    warning_messages: list[str] = list()
    if (args.threshold <= 0):
        warning_messages.append(f'WARNING! Threshold value ({args.threshold}) is <= 0. All rolls will succeed.')
    elif (args.threshold > DIE_SIZE):
        warning_messages.append(f'WARNING! Threshold value ({args.threshold}) is above max die value ({DIE_SIZE}). All rolls will fail.')
    if not args.bumps and not args.drops:
        warning_messages.append('WARNING! No bumps or drops applied.')
    if (warning_messages):
        for msg in warning_messages:
            print(msg)
        if not getBooleanUserInput("Proceed anyway?"):
            exit(0)
    
    # Do the work
    roll_simulator: RollSimulator = RollSimulator(args.num_dice, args.threshold,
                                                  (args.bumps - args.drops))
    roll_simulator.compute_roll_odds()
    for line in roll_simulator.get_printable_result(
            include_roll_details=args.print_roll_details):
        print(line)


if __name__ == "__main__":
    main()