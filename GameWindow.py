from tkinter import *
from game import *
from functools import partial


window = None
buttons = []
text_label = None
bunny_photo = None
grass_photo = None
kid_photo = None


def construct_window():
    global window
    global buttons
    global bunny_photo
    global kid_photo
    global grass_photo

    window = Tk()

    window.title('Catch the bunny Game')

    frame = Frame(window)
    frame.grid()

    # Initialize the buttons list
    buttons = [[0 for i in range(BOARD_LENGTH)] for j in range(BOARD_LENGTH)]

    # load the background, kid and bunny images
    bunny_photo = PhotoImage(file = r"images/bunny.png")
    grass_photo = PhotoImage(file = r"images/grass.png")
    kid_photo = PhotoImage(file = r"images/kid.png")

    # create the board's buttons
    for i in range(BOARD_LENGTH):
        for j in range(BOARD_LENGTH):
            buttons[i][j] = Button(frame, height=80, width=120, image=grass_photo, bg='pale turquoise1', command= partial(player_move,i, j))
            buttons[i][j].grid(column=j, row=i)

    # set the kid and the bunny initial positions
    update_new_positions(kid_photo, bunny_photo)


def change_image(row, col, image):
    buttons[row][col].config(image=image, compound=TOP)
    buttons[row][col].grid(column=col,row=row)


def update_new_positions(new_photo_kid, new_photo_bunny):
    bunny_row = get_bunny_row()
    bunny_col = get_bunny_col()
    change_image(bunny_row, bunny_col, new_photo_bunny)

    kid_row = get_kid_row()
    kid_col = get_kid_col()
    change_image(kid_row, kid_col, new_photo_kid)


count = 1


def player_move(row, col):
    global count
    print('player_move ',count, '. row', row, ' col ', col)
    count = count + 1

    if validate_kid_move(row, col) is False:
        print('illegal move!!!!!!!!!!!')
        return

    # reset the previous kid and bunny positions
    update_new_positions(grass_photo, grass_photo)

    # play a round
    game_state = play_round(row, col)

    # update the new kid and bunny positions
    update_new_positions(kid_photo, bunny_photo)

    # check if the game is over
    if game_state is GameState.COMPUTER_WON:
        print('bunny won!')
        show_game_over_message('bunny won!')
    elif game_state is GameState.PLAYER_WON:
        print('player won!')
        show_game_over_message('player won!')


def show_game_over_message(text):
    global text_label
    text_label = Label(window, width=45, text=text, font=("Helvetica", 18))
    text_label.grid(row=0)


# initialize the game parameter
init_game()

construct_window()
window.mainloop()
