import random
from enum import Enum


class MoveDirection(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
    ILLEGAL_MOVE = 5


class GameState(Enum):
    IN_PROGRESS = 1
    PLAYER_WON = 2
    COMPUTER_WON = 3
    ILLEGAL_MOVE = 4


# ---- game constants
MAX_NUM_OF_MOVES = 10
BOARD_LENGTH = 9
BOARD_SIZE = BOARD_LENGTH * BOARD_LENGTH

# --- game parameters
kid_row = 0
kid_col = 0
bunny_row = 0
bunny_col = 0
number_of_moves = 0


def init_game():
    global kid_row
    global kid_col
    global bunny_row
    global bunny_col
    global number_of_moves

    kid_row = 0
    kid_col = 0
    bunny_row = 0
    bunny_col = 0
    number_of_moves = 0

    # Set a spot for the bunny
    init_locations()


# Change the initial position (in case the randomized positions are the same - set them to be different)
def move_initial_position():
    global bunny_row
    global bunny_col

    bunny_row = BOARD_SIZE - kid_row
    bunny_col = BOARD_SIZE - kid_col


def init_locations():
    global bunny_row
    global bunny_col
    global kid_row
    global kid_col

    # generate a position for the kid
    position = random.randint(0, BOARD_SIZE)
    kid_row = int(position / BOARD_LENGTH)
    kid_col = int(position % BOARD_LENGTH)

    # generate a position for the bunny
    position = random.randint(0, BOARD_LENGTH)
    new_row = int(position / BOARD_LENGTH)
    new_col = int(position % BOARD_LENGTH)

    # Verify that the positions are different
    if new_row == kid_row and new_col == kid_col:
        move_initial_position()
    else:
        bunny_row = new_row
        bunny_col = new_col


# Validate the chosen new cell is allowed (one cell up\dowm\left\right)
def validate_kid_move(row, col):
    if abs(kid_row - row) + abs(kid_col - col) is not 1:
        return False
    else:
        return True


def update_move(new_row, new_col):
    global kid_col
    global kid_row

    kid_col = new_col
    kid_row = new_row


# generates a random legal move for the computer
def generate_random_move():
    global bunny_col
    global bunny_row

    direction = random.randint(1, MoveDirection.__len__())
    direction = MoveDirection(direction)

    if direction == MoveDirection.UP:
        if bunny_col < BOARD_LENGTH - 1:
            bunny_col = bunny_col + 1
        else:  # the bunny is in the most upper column - move it down one step
            bunny_col = BOARD_LENGTH - 2
    elif direction == MoveDirection.DOWN:
        if bunny_col > 0:
            bunny_col = bunny_col - 1
        else:  # the bunny is in the most lower column - move it up one step
            bunny_col = 1
    elif direction == MoveDirection.LEFT:
        if bunny_row > 0:
            bunny_row = bunny_row - 1
        else:  # the bunny is in the upper column - move it down
            bunny_row = 1
    else:  # direction = MoveDirection.RIGHT:
        if bunny_row < BOARD_LENGTH - 1:
            bunny_row = bunny_row + 1
        else:  # the bunny is in the upper column - move it down
            bunny_row = bunny_row - 2


def calc_distance_to_kid(row, col):
    return abs(col - kid_col) + abs(row - kid_row)


# parameters related to the calculation of the bunny move
row_of_max = 0
col_of_max = 0
max_distance = 0


def init_max_position_params():
    global row_of_max
    global col_of_max
    global max_distance

    row_of_max = 0
    col_of_max = 0
    max_distance = 0


def update_max_dist_from_kid(current_dist, row, col):
    global row_of_max
    global col_of_max
    global max_distance

    if current_dist > max_distance:
        row_of_max = row
        col_of_max = col
        max_distance = current_dist


def generate_smart_move():
    global bunny_col
    global bunny_row

    current_col = 0
    current_row = 0
    current_distance = 0

    init_max_position_params()

    # Calculate the distance between the kid and the bunny in the 4 situations and choose the max

    # Calculate up direction
    if bunny_col < BOARD_LENGTH - 1:
        current_col = bunny_col + 1
        current_row = bunny_row
        current_distance = calc_distance_to_kid(current_row, current_col)
        update_max_dist_from_kid(current_distance, current_row, current_col)

    # Calculate down direction
    if bunny_col > 0:
        current_col = bunny_col - 1
        current_row = bunny_row
        current_distance = calc_distance_to_kid(current_row, current_col)
        update_max_dist_from_kid(current_distance, current_row, current_col)

    # Calculate left direction
    if bunny_row > 0:
        current_col = bunny_col
        current_row = bunny_row - 1
        current_distance = calc_distance_to_kid(current_row, current_col)
        update_max_dist_from_kid(current_distance, current_row, current_col)

    # Calculate right direction
    if bunny_row < BOARD_LENGTH - 1:
        current_col = bunny_col
        current_row = bunny_row + 1
        current_distance = calc_distance_to_kid(current_row, current_col)
        update_max_dist_from_kid(current_distance, current_row, current_col)

    # finally update the bunny's positions to the best one
    bunny_row = row_of_max
    bunny_col = col_of_max


def get_kid_row():
    return kid_row


def get_kid_col():
    return kid_col


def get_bunny_row():
    return bunny_row


def get_bunny_col():
    return bunny_col


def kid_caught_bunny():
    if bunny_col == kid_col and bunny_row == kid_row:
        return True
    return False


# One round includes one turn of the kid and one turn of the bunny (computer)
def play_round(row,col):
    global number_of_moves

    # Update the kid's move
    update_move(row, col)

    # increase the number of attempts
    number_of_moves = number_of_moves + 1

    # check if the kid won
    if kid_caught_bunny():
        return GameState.PLAYER_WON

    # check if the game there are more attempts to catch the bunny
    if number_of_moves == MAX_NUM_OF_MOVES:
        return GameState.COMPUTER_WON

    # the game is still on - generate a move for the bunny
    # generate_random_move()
    generate_smart_move()

    return GameState.IN_PROGRESS









