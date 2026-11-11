import argparse
from rpgse_221132 import DIE_SIZE, get_boolean_user_input, RollSimulator
import sys

def main():
    """See argparse description."""
    parser = argparse.ArgumentParser(
                    prog='rpgse_221132_single_roll_tester',
                    description=f'''
Test what happens to a single roll under the bump/drop system described in https://rpg.stackexchange.com/q/221132/.

Given a specific roll of the dice, threshold value, number of bumps, and number of drops, this program applies the
bump/drop logic from the base rpgse_221132 program and shows you how it affects that roll.''',
                    formatter_class=argparse.RawTextHelpFormatter)
    roll_params_group = parser.add_argument_group('Roll parameters', 'Tell the program what roll to modify, and how.')
    roll_params_group.add_argument('-r', '--roll', type=int, required=True, nargs='+',
                        help=f'A series of numbers between 1 and {DIE_SIZE} (inclusive), representing a particular roll of dice.')
    roll_params_group.add_argument('-t', '--threshold', type=int, required=True,
                        help='Number that a die must equal or exceed to count as a success.')
    roll_params_group.add_argument('-b', '--bumps', type=int, default=0,
                        help='The number of "bumps" (plus-ones) to apply to dice after the roll.')
    roll_params_group.add_argument('-d', '--drops', type=int, default=0,
                            help='The number of "drops" (minus-ones) to apply to dice after the roll.')
    args = parser.parse_args()
    
    # Input validation
    # Error states
    print(f'args: {args}')
    num_dice = len(args.roll)
    if (num_dice < 1):
        print('ERROR! Number of dice cannot be less than 1.', file=sys.stderr)
        exit(1)
    for die_value in args.roll:
        if die_value < 1 or die_value > DIE_SIZE:
            print(f'ERROR! {die_value} is not between 1 and {DIE_SIZE}.', file=sys.stderr)
            exit(2)
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
        if not get_boolean_user_input("Proceed anyway?"):
            exit(0)

    # Do the work
    args.roll.sort()
    print(f'Modifying the roll {args.roll}, '
          + f'successes >= {args.threshold}, '
          + f'{args.bumps} bump{'' if args.bumps == 1 else 's'} '
          + f'and {args.drops} drop{'' if args.drops == 1 else 's'}...')
    roll_simulator: RollSimulator = RollSimulator(num_dice, args.threshold,
                                                  (args.bumps - args.drops))
    result = roll_simulator._bump_and_drop_rolls(tuple(args.roll)) # pyright: ignore[reportPrivateUsage]
    print(f'Changed {args.roll} to {result}')


if __name__ == "__main__":
    main()