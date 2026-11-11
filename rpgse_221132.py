import argparse
from collections import Counter
from decimal import Decimal
from itertools import product
import sys
from textwrap import indent
from typing import Any, Callable, Sequence

DIE_SIZE: int = 6
BLOCK_CHAR: str = '\u2588'
INDENT = '    '
MAX_OUTPUT_LINE_LEN = 120
ROLL_BLOCK_SIZE = 1_000_000

class RollSimulator(object):
    """Rolls dice, applies bumps/drops, and counts the results."""

    def __init__(self, dice_per_roll: int, threshold: int, roll_mod: int):
        self._raw_roll_counts: Counter[tuple[int, ...]] = Counter()
        self._modded_roll_counts: Counter[tuple[int, ...]] = Counter()
        self._summarized_roll_counts: Counter[tuple[int, ...]] = Counter()
        self._dice_per_roll = dice_per_roll
        self._threshold = threshold
        self._roll_mod = roll_mod

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
    
    def _compute_roll_odds(self):
        # Don't run this if we done it already, or if the result will be empty
        if self._summarized_roll_counts or self._dice_per_roll < 1:
            return

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

        # For the "summarized" results, converts the modded roll outcomes into
        # (# of successes, # of max-values) tuples, and total those counts.
        for k, v in self._modded_roll_counts.items():
            num_successes: int = 0
            num_maxes: int = 0
            die: int
            for die in k:
                if (die >= self._threshold):
                    num_successes += 1
                if (die == DIE_SIZE):
                    num_maxes += 1
            self._summarized_roll_counts[(num_successes, num_maxes)] += v

    def get_summarized_results(self) -> Counter[tuple[int, ...]]:
        '''
        Returns a new Counter object with the proportional odds of each result type.
        
        "Result type" is represented by the tuple: (&lt;number of successes rolled&gt;,
        &lt;number of max-values rolled&gt).
        
        "Proportional odds": e.g. if a (1,1) result is three times as likely as
        a (2,1) result, the counter will be something like {(1,1): 3, (2,1): 1, ...}
        or {(1,1): 6, (2,1): 2, ...}
        '''
        self._compute_roll_odds()
        return Counter(self._summarized_roll_counts)
    
    def get_full_results(self) -> Counter[tuple[int, ...]]:
        '''
        Returns a new Counter object with the proportional odds of each roll outcome.
        
        A "roll outcome" is any possible combination of dice values that can result
        from rolling the given number of dice and applying the bumps and drops.
        This is presented as a sorted tuple.
        E.g. for 3 dice with threshold 3 and 1 bump, (2,3,6), (1,1,5), and (3,6,6)
        are all possible roll outcomes.
        But (2,2,2) is not possible, because a pre-bump roll of (2,2,2) would have
        been bumped to (2,2,3), and a pre-bump roll of (1,2,2) would not have been
        bumped at all. (We stop applying bumps and drops if they won't change the
        number of successes or the number of max-values.)
        
        "Proportional odds": e.g. if a (1,1) result is three times as likely as
        a (2,1) result, the counter will be something like {(1,1): 3, (2,1): 1, ...}
        or {(1,1): 6, (2,1): 2, ...}
        '''
        self._compute_roll_odds()
        return Counter(self._modded_roll_counts)

def stringify_proportional_odds(odds_counter: Counter[Any], sort_by_odds: bool,
                                no_bars: bool, full_bars: bool) -> list[str]:
    '''
    Convert the proportional number to a percentage number, and also tack on a
    visual "bar graph" made of block characters.
    '''
    percent_strings: list[str] = []
    lines: list[str] = []

    # Sort by keys asc. if sort_by_odds is false, and values desc. if it's true
    sortable_odds_counts: list[tuple[Any, int]] = list(odds_counter.items())
    sort_key: Callable[[tuple[Any, int]], Any] = \
            (lambda x: x[1]) if sort_by_odds else (lambda x: x[0])
    sortable_odds_counts.sort(key=sort_key, reverse=sort_by_odds)

    max_percent_str_len: int = -1
    for item in sortable_odds_counts:
        k: Any = item[0]
        v: int = item[1]
        fraction: Decimal = Decimal(v) / Decimal(odds_counter.total())
        percent_str: str = f'{k}: {fraction * 100:.3}%'
        percent_strings.append(percent_str)
        if not no_bars:
            max_percent_str_len = max(len(percent_str), max_percent_str_len)
    if not no_bars:
        # Figure out how long a bar is allowed to be.
        # We have a simple default func, where length == count:
        get_bar_length_from_count: Callable[[int], int] = lambda x: x
        if not full_bars:
            # '+ 1' for the space between the (longest) percent and the bars
            max_bar_length = MAX_OUTPUT_LINE_LEN - max_percent_str_len + 1
            max_count = max(odds_counter.values())
            if max_count > max_bar_length:
                # Replace the default func with a more complex one.
                # We should "compress" each bar to fit in the allotted range.
                ratio: Decimal = Decimal(max_bar_length) / Decimal(max_count)
                get_bar_length_from_count = lambda x: round(Decimal(x) * ratio)
        # Then finally build the lines
        for percent_str, count in zip(percent_strings, (item[1] for item in sortable_odds_counts)):
            len_diff: int = max_percent_str_len - (len(percent_str))
            padding: str = ' ' * len_diff # 0 for the longest line(s)
            bar_str: str = ' ' + (BLOCK_CHAR * get_bar_length_from_count(count))
            lines.append(percent_str + padding + bar_str)
    else:
        lines = percent_strings
    return lines

def get_printable_results(rs: RollSimulator, do_print_full_results: bool,
                          sort_by_odds: bool, no_bars: bool, full_bars: bool) -> list[str]:
    lines: list[str] = []

    # Results by successes + maxes
    lines.append(f'Final roll odds grouped by (# successes, # {DIE_SIZE}s):')
    summary_lines = (indent(s, INDENT)
                        for s
                        in stringify_proportional_odds(
                            rs.get_summarized_results(), sort_by_odds, no_bars, full_bars))
    lines.extend(summary_lines)

    # Results by roll
    if (do_print_full_results):
        lines.append('Roll odds for specific rolls (after bumping and dropping):')
        modded_detail_lines = (indent(s, INDENT)
                                for s
                                in stringify_proportional_odds(
                                    rs.get_full_results(), sort_by_odds, no_bars, full_bars))
        lines.extend(modded_detail_lines)
    
    return lines

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
                    description='''
Computes odds of rolls under the bump/drop system described in https://rpg.stackexchange.com/q/221132/.

The idea of the system is that you roll a number of 6-sided dice, apply "bumps" and "drops", (+1 and -1
modifiers), and see how many are successes (greater than or equal to the "threshold" number). 6s have
bonus properties. Dies may be bumped or dropped more than once.

For a given number of dice, threshold value, number of bumps, and number of drops, this program computes
the odds of every possible outcome. First, it finds every possible "raw" roll. Then it cancels out the
bumps and drops until only one side remains, and applies those "nudges" to each possible roll in turn.
Nudges are applied to maximize/minimize the number of successes first; if any nudges are left over, the
program then tries to create/remove 6s. Any nudges left over after that are not applied, as they cannot
change the outcome. Finally, rolls with the same numbers of successes and 6s are grouped together, and
the program prints the odds of landing in each group, with an approximate bar graph for illustration.''',
                    formatter_class=argparse.RawTextHelpFormatter)
    roll_params_group = parser.add_argument_group('Roll parameters', 'Tell the program what rolls to simulate.')
    roll_params_group.add_argument('-n', '--num-dice', type=int, required=True,
                        help='The number of d6 dice to roll (>=1).')
    roll_params_group.add_argument('-t', '--threshold', type=int, required=True,
                        help='Number that a die must equal or exceed to count as a success.')
    roll_params_group.add_argument('-b', '--bumps', type=int, default=0,
                        help='The number of "bumps" (plus-ones) to apply to dice after the roll.')
    roll_params_group.add_argument('-d', '--drops', type=int, default=0,
                            help='The number of "drops" (minus-ones) to apply to dice after the roll.')
    result_formatting_group = parser.add_argument_group('Result formatting', 'Change how the program prints out its results.')
    result_formatting_group.add_argument('--full-details', action='store_true',
                            help='Print chance of each distinct roll. (This may be very long.)')
    result_formatting_group.add_argument('-s', '--sort', type=str, choices=('R', 'r', 'O', 'o'), default='R',
                            help='''
Choose the sort mode for the results. Accepted values are:
  - 'R': sort the results by the roll type / roll. E.g. (1,1) before (1,2).
     This is the default.
  - 'O': sort the results by their odds, from most likely to least.
     E.g. 10%% before 9%%.
  - 'r' and 'o': aliases for 'R' and 'O' respectively.''')
    
    bar_graph_subgroup = result_formatting_group.add_mutually_exclusive_group()
    bar_graph_subgroup.add_argument('--no-bars', action='store_true',
                            help='Turn off the bar graph in the results.')
    bar_graph_subgroup.add_argument('--full-bars', action='store_true',
                            help='''
Show the bars in the bar graph at their full / true lengths,
instead of compressing them to fit in a more reasonable width.
This is technically more accurate but may be harder to look at.''')
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
    sort_by_odds: bool = (args.sort.upper() == 'O')
    for line in get_printable_results(roll_simulator, args.full_details,
                                      sort_by_odds, args.no_bars, args.full_bars):
        print(line)


if __name__ == "__main__":
    main()