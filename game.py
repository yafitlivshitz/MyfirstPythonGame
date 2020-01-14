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
kid_position = (0, 0)
bunny_position = (0, 0)
number_of_moves = 0


def init_game():
    global number_of_moves

    number_of_moves = 0

    init_locations()


def generate_random_position():
    position = random.randint(0, BOARD_SIZE)

    return int(position / BOARD_LENGTH), int(position % BOARD_LENGTH)


def change_initial_bunny_position():
    global bunny_position

    bunny_position[0] = BOARD_SIZE - kid_position[0]
    bunny_position[1] = BOARD_SIZE - kid_position[1]


def init_locations():
    global kid_position
    global bunny_position

    kid_position = generate_random_position()
    bunny_position = generate_random_position()

    if kid_caught_bunny():
        change_initial_bunny_position()


# Validate the chosen new cell is allowed (one cell up\down\left\right)
def validate_kid_move(row, col):
    if distance_to_kid((row, col)) is not 1:
        return False
    else:
        return True


def is_bunny_on_upper_boarder():
    return bunny_position[0] == 0


def is_bunny_on_down_boarder():
    return bunny_position[0] == BOARD_LENGTH - 1


def is_bunny_on_left_boarder():
    return bunny_position[1] == 0


def is_bunny_on_right_boarder():
    return bunny_position[1] == BOARD_LENGTH - 1


def generate_random_move():
    global bunny_position

    direction = random.randint(1, MoveDirection.__len__())
    direction = MoveDirection(direction)

    if direction == MoveDirection.UP:
        if is_bunny_on_upper_boarder():
            bunny_position = (1, bunny_position[1])
        else:
            bunny_position = (bunny_position[0] - 1, bunny_position[1])

    elif direction == MoveDirection.DOWN:
        if is_bunny_on_down_boarder():
            bunny_position = (BOARD_LENGTH - 2, bunny_position[1])
        else:
            bunny_position = (bunny_position[0] + 1, bunny_position[1])
    elif direction == MoveDirection.LEFT:
        if is_bunny_on_left_boarder():
            bunny_position = (bunny_position[0], 1)
        else:  # the bunny is in the upper column - move it down
            bunny_position = (bunny_position[0], bunny_position[1] - 1)
    else:  # direction = MoveDirection.RIGHT:
        if is_bunny_on_right_boarder():
            bunny_position = (bunny_position[0], BOARD_LENGTH - 2)
        else:  # the bunny is in the upper column - move it down
            bunny_position = (bunny_position[0], bunny_position[1] + 1)

    # todo: check that the bunny is not on the kid's position


def distance_to_kid(position):
    return abs(kid_position[0] - position[0]) + abs(kid_position[1] - position[1])


# parameters related to the calculation of the bunny move
max_distance_position = (0, 0)
max_distance = 0


def init_max_position_params():
    global max_distance_position
    global max_distance

    max_distance_position = (0, 0)
    max_distance = 0


def update_max_dist_from_kid(current_dist, position):
    global max_distance_position
    global max_distance

    if current_dist > max_distance:
        max_distance_position = position
        max_distance = current_dist


def check_max_distance_to_kid(position):
    current_distance = distance_to_kid(position)
    update_max_dist_from_kid(current_distance, position)


def generate_smart_move():
    global bunny_position

    init_max_position_params()

    # Calculate the distance between the kid and the bunny in the 4 situations and choose the max

    # Calculate up direction
    if is_bunny_on_upper_boarder() is False:
        check_max_distance_to_kid((bunny_position[0] - 1, bunny_position[1]))

    # Calculate down direction
    if is_bunny_on_down_boarder() is False:
        check_max_distance_to_kid((bunny_position[0] + 1, bunny_position[1]))

    # Calculate left direction
    if is_bunny_on_left_boarder() is False:
        check_max_distance_to_kid((bunny_position[0], bunny_position[1] - 1))

    # Calculate right direction
    if is_bunny_on_right_boarder() is False:
        check_max_distance_to_kid((bunny_position[0], bunny_position[1] + 1))

    # finally update the bunny's positions to the best one
    bunny_position = (max_distance_position[0], max_distance_position[1])


def get_kid_row():
    return kid_position[0]


def get_kid_col():
    return kid_position[1]


def get_bunny_row():
    return bunny_position[0]


def get_bunny_col():
    return bunny_position[1]


def kid_caught_bunny():
    if bunny_position[0] == kid_position[0] and bunny_position[1] == kid_position[1]:
        return True
    return False


# One round includes one turn of the kid and one turn of the bunny (computer)
def play_round(row, col):
    global number_of_moves
    global kid_position

    kid_position = (row, col)

    number_of_moves = number_of_moves + 1

    if kid_caught_bunny():
        return GameState.PLAYER_WON

    if number_of_moves == MAX_NUM_OF_MOVES:
        return GameState.COMPUTER_WON

    # generate_smart_move()
    generate_random_move()

    return GameState.IN_PROGRESS
