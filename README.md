# RPGSE_221132

Computes odds of dice rolls under the RPG system described in https://rpg.stackexchange.com/q/221132/.

The idea of the system is that you roll a number of 6-sided dice, apply "bumps" and "drops", (+1 and -1 modifiers), and count how many dice are successes (greater than or equal to the "threshold" number). 6s have bonus properties. A die may be bumped or dropped more than once.

For a given number of dice, threshold value, number of bumps, and number of drops, this program computes the odds of every possible outcome. First, it finds every possible "raw" roll. Then it cancels out the bumps and drops until only one side remains, and applies those "nudges" to each possible roll in turn. Nudges are applied to maximize/minimize the number of successes first; if any nudges are left over, the program then tries to create/remove 6s. Any nudges left over after that are not applied, as they cannot change the outcome. Finally, rolls with the same numbers of successes and 6s are grouped together, and the program prints the odds of landing in each group, with an approximate bar graph for illustration.

```powershell
PS C:\Users\foo\bar> python .\rpgse_221132.py -n 3 -t 4 -b 3 -d 1 --sort O
Working with 3 dice, successes >= 4, 3 bumps and 1 drop...
Final roll odds grouped by (# successes, # 6s):
    (2, 1): 19.4%  ██████████████████████████████████████████
    (2, 0): 17.1%  █████████████████████████████████████
    (3, 1): 15.7%  ██████████████████████████████████
    (3, 2): 11.6%  █████████████████████████
    (3, 0): 9.72%  █████████████████████
    (1, 0): 8.80%  ███████████████████
    (2, 2): 8.33%  ██████████████████
    (3, 3): 4.63%  ██████████
    (1, 1): 4.17%  █████████
    (0, 0): 0.463% █
```

## Bump/drop logic examples:

Altered values are bolded. 6s are in italics.

### Bumps, 3 dice:

| Raw roll | Hit Threshold (HT) | Bumps (+1)| Drops (-1) | Final roll |
|----------|--------------------|-----------|------------|------------|
| (1, 1, 5) | 3 | 1    | 0 | (1, 1, **_6_**) |
| (1, 1, 5) | 3 | 2    | 0 | (1, **3**, 5) |
| (1, 1, 5) | 3 | 3    | 0 | (1, **3**, **_6_**) |
| (1, 1, 5) | 3 | 4    | 0 | (**3**, **3**, 5) |
| (1, 1, 5) | 3 | 5-7  | 0 | (**3**, **3**, **_6_**) |
| (1, 1, 5) | 3 | 8-10 | 0 | (**3**, **_6_**, **_6_**) |
| (1, 1, 5) | 3 | 11+  | 0 | (**_6_**, **_6_**, **_6_**) |

### Drops, 3 dice:

| Raw roll | Hit Threshold (HT) | Bumps (+1)| Drops (-1) | Final roll |
|----------|--------------------|-----------|------------|------------|
| (4, 5, _6_) | 3 | 0 | 1   | (4, 5, **5**) |
| (4, 5, _6_) | 3 | 0 | 2   | (**2**, 5, _6_) |
| (4, 5, _6_) | 3 | 0 | 3-4 | (**2**, 5, **5**) |
| (4, 5, _6_) | 3 | 0 | 5   | (**2**, **2**, _6_) |
| (4, 5, _6_) | 3 | 0 | 6-8 | (**2**, **2**, **5**) |
| (4, 5, _6_) | 3 | 0 | 9+  | (**2**, **2**, **2**) |

### Bumps, threshold 3 vs. threshold 4 

| Raw roll | Hit Threshold (HT) | Bumps (+1)| Drops (-1) | Final roll |
|----------|--------------------|-----------|------------|------------|
| (1, 4) | 3 | 1  | 0 | (1, 4) |
| (1, 4) | 3 | 2  | 0 | (**3**, 4) |
| (1, 4) | 3 | 3  | 0 | (**3**, 4) |
| (1, 4) | 3 | 4  | 0 | (**3**, **_6_**) |
| (1, 4) | 3 | 5  | 0 | (**3**, **_6_**) |
| (1, 4) | 3 | 6  | 0 | (**3**, **_6_**) |
| (1, 4) | 3 | 7+ | 0 | (**_6_**, **_6_**) |
| -      | - | -  | - | - |
| (1, 4) | 4 | 1  | 0 | (1, 4) |
| (1, 4) | 4 | 2  | 0 | (1, **_6_**) |
| (1, 4) | 4 | 3  | 0 | (**4**, 4) |
| (1, 4) | 4 | 4  | 0 | (**4**, 4) |
| (1, 4) | 4 | 5  | 0 | (**4**, **_6_**) |
| (1, 4) | 4 | 6  | 0 | (**4**, **_6_**) |
| (1, 4) | 4 | 7+ | 0 | (**_6_**, **_6_**) |

### Bumps >= drops:

| Raw roll | Hit Threshold (HT) | Bumps (+1)| Drops (-1) | Final roll |
|----------|--------------------|-----------|------------|------------|
| (2, 2, 2) | 3 | 3   | 3   | (2, 2, 2) |
| (2, 2, 2) | 3 | 3   | 2   | (2, 2, **3**) |
| (2, 2, 2) | 3 | 3   | 1   | (2, **3**, **3**) |
| (2, 2, 2) | 3 | 3   | 0   | (**3**, **3**, **3**) |
| (2, 2, 2) | 3 | 4   | 1   | (**3**, **3**, **3**) |
| (2, 2, 2) | 3 | 5   | 2   | (**3**, **3**, **3**) |
| (2, 2, 2) | 3 | 6   | 3   | (**3**, **3**, **3**) |
| (2, 2, 2) | 3 | 999 | 996 | (**3**, **3**, **3**) |

### Bumps <= drops:

| Raw roll | Hit Threshold (HT) | Bumps (+1)| Drops (-1) | Final roll |
|----------|--------------------|-----------|------------|------------|
| (3, 3, 3) | 3 | 3   | 3   | (3, 3, 3) |
| (3, 3, 3) | 3 | 2   | 3   | (**2**, 3, 3) |
| (3, 3, 3) | 3 | 1   | 3   | (**2**, **2**, 3) |
| (3, 3, 3) | 3 | 0   | 3   | (**2**, **2**, **2**) |
| (3, 3, 3) | 3 | 1   | 4   | (**2**, **2**, **2**) |
| (3, 3, 3) | 3 | 2   | 5   | (**2**, **2**, **2**) |
| (3, 3, 3) | 3 | 3   | 6   | (**2**, **2**, **2**) |
| (3, 3, 3) | 3 | 996 | 999 | (**2**, **2**, **2**) |

