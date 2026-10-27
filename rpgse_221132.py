import argparse
from collections import Counter
##### from math import comb
from random import randint
import sys
from textwrap import indent
from typing import Any

DIE_SIZE: int = 6
INDENT = '    '

class RollSimulator(object):
    """Rolls dice, applies bumps/drops, and tracks the results."""

    
    def __init__(self, dice_per_roll: int, threshold: int, roll_mod: int):
        self._final_roll_counts: Counter[tuple[int, ...]] = Counter()
        self._dice_per_roll = dice_per_roll
        self._threshold = threshold
        self._roll_mod = roll_mod

        
    def _stringify_counter_as_percents(self, counter: Counter[Any]) -> str:
        result_str = ''
        k: Any
        for k in sorted(counter):
            fraction: float = counter[k] / counter.total()
            result_str += f'{k}: {fraction * 100}\n'
        return result_str

    
    def _count_results_by_successes_and_maxes(self) -> Counter[tuple[int, int]]:
        """
        Converts the known roll outcomes into (# of successes, # of max-values)
        tuples, and then counts the numbers of each. 
        """
        successes_and_maxes_counts: Counter[tuple[int, int]] = Counter()
        k: tuple[int, ...]
        v: int
        for k, v in self._final_roll_counts.items():
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

        
    def get_result(self) -> str:
        result_str = f'Simulated {self._final_roll_counts.total()} rolls.\n'
        
        # Results by successes + maxes
        result_str += f'Percent by (# successes, # {DIE_SIZE}s):\n'
        result_str += indent(self._stringify_counter_as_percents(
            self._count_results_by_successes_and_maxes()), INDENT)
        
        # Results by roll
        result_str += 'Percent by final (modified) roll:\n'
        result_str += indent(self._stringify_counter_as_percents(
            self._final_roll_counts), INDENT)
        
        return result_str


    def _roll_dice(self) -> list[int]:
        rolls = [randint(1, DIE_SIZE) for _ in range(self._dice_per_roll)]
        rolls.sort()
        return rolls
    
    def _bump_and_drop_rolls(self, rolls: list[int]) -> tuple[int, ...]:
        # TODO: actually add the bumps and drops
        return tuple(rolls)
    
    def do_rolls(self, num_rolls: int):
        for _ in range(num_rolls):
            modded_roll: tuple[int, ...] = self._bump_and_drop_rolls(
                self._roll_dice())
            self._final_roll_counts[modded_roll] += 1
            


def main():
    parser = argparse.ArgumentParser(
                    prog='rpgse_221132_monte_carlo',
                    description='Simulates a large number of dice rolls under the bump/drop system described in https://rpg.stackexchange.com/q/221132/ to find a roughly-average result.')
    parser.add_argument('-n', '--num-dice', type=int, required=True,
                        help='The number of d6 dice to roll')
    parser.add_argument('-t', '--threshold', type=int, required=True,
                        help='Number that a die must equal or exceed to count as a Success')
    parser.add_argument('-b', '--bumps', type=int, default=0,
                        help='The number of "bumps" (plus-ones) to apply to dice after the roll')
    parser.add_argument('-d', '--drops', type=int, default=0,
                            help='The number of "drops" (minus-ones) to apply to dice after the roll')
    parser.add_argument('-r', '--num-rolls', type=int, default=100_000,
                            help='The number of rolls to simulate')
    args = parser.parse_args()
    
    # Input validation
    # Error states
    if (args.num_dice < 0):
        print('ERROR! Number of dice cannot be negative.', file=sys.stderr)
        exit(1)
    if (args.bumps < 0 or args.drops < 0):
        print('ERROR! Bumps and/or drops cannot be negative numbers.', file=sys.stderr)
        exit(2)
    # Warning states
    warning_msg: str = ''
    if (args.threshold <= 0):
        warning_msg = f'WARNING! Threshold value ({args.threshold}) is <= 0. Results may not be useful.'
    elif (args.threshold > DIE_SIZE):
        warning_msg = f'WARNING! Threshold value ({args.threshold}) is above max die value. Results may not be useful.'
    if (warning_msg):
        print(warning_msg)
        while True:
            response: str = input("Proceed anyway? [Y/N] ")
            if (response == 'Y' or response == 'y'):
                break
            elif (response == 'N' or response == 'n'):
                exit(0)
    
    # Do the work
    roll_simulator: RollSimulator = RollSimulator(args.num_dice, args.threshold,
                                                  (args.bumps - args.drops))
    # TODO: calculate reasonable number of rolls to simulate?
    # Number of possible raw roll outcomes: {DIE_SIZE} multichoose {num_dice}
    # i.e.: ({DIE_SIZE} + {num_dice} - 1) choose {num_dice}
    ##### print(comb(DIE_SIZE + args.num_dice - 1, args.num_dice))
    roll_simulator.do_rolls(args.num_rolls)
    # TODO: BUG! Doesn't print all rolls when num_rolls is too high
    print(roll_simulator.get_result())
    exit(0)

if __name__ == "__main__":
    main()