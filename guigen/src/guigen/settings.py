GOAL = "-"
MAX_DEPTH = 5
GRID_SIZE = 4

# The probability that a button will generate as the goal.
# Max one goal on page. Min one goal for generation.
# The goal is guaranteed on the last page.
# This essentially effects how likely buttons will
# generate before the last page.
GOAL_PROBABILITY = 0.1

# Character set to generate button text from.
# Currently, the GOAL should not be in this set.
CHARSET = __import__("string").ascii_uppercase
