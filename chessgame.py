# Chess game with all the moves and rules of normal chess
# Has a PGN editor feature
# Created for: Python 3.8
# Implemented using: tkinter and numpy
# Date Created: Summer 2020

from tkinter import *
from tkinter import messagebox
import tkinter.font as tkfont
import numpy as np

root = Tk()
root.title("Chessboard")
root.resizable(False, False)
root.geometry("1000x800")

b_rook = PhotoImage(file='assets/b_rook.png')
w_rook = PhotoImage(file='assets/w_rook.png')
w_king = PhotoImage(file='assets/w_king.png')
b_king = PhotoImage(file='assets/b_king.png')
w_queen = PhotoImage(file='assets/w_queen.png')
b_queen = PhotoImage(file='assets/b_queen.png')
w_knight = PhotoImage(file='assets/w_knight.png')
b_knight = PhotoImage(file='assets/b_knight.png')
w_bishop = PhotoImage(file='assets/w_bishop.png')
b_bishop = PhotoImage(file='assets/b_bishop.png')
w_pawn = PhotoImage(file='assets/w_pawn.png')
b_pawn = PhotoImage(file='assets/b_pawn.png')
pixelVirtual = PhotoImage(width=1, height=1)

w = 1000
h = 1000

board_color_light = 'white'
board_color_dark = '#057815'

# these need to be different
piece_bg_white = 'white'
piece_bg_black = '#3f3f3f'

if piece_bg_black == piece_bg_white:
    raise Exception("Piece colors need to be different")

canvas = Canvas(root, width=w, height=h, bg='lightgrey')
canvas.pack()
font_style = tkfont.Font(family="System", size=16)

piece_list = []
color_list = []
pawn_moved_black = []
pawn_moved_white = []
king_moved_ = []
rook_moved_ = []
en_passant_list = []
piece_object_list = []
current_move = 1
en_passant_last = 0
king_check_last = 0
non_capture_moves = 0
successful_block = False
editor_enabled = False
editor_canvas = Canvas()


def initialize_board():
    global piece_list
    global color_list
    global pawn_moved_black
    global pawn_moved_white
    global king_moved_
    global rook_moved_
    global current_move
    global en_passant_last
    global en_passant_list
    global king_check_last
    global successful_block
    global editor_enabled
    global non_capture_moves
    global piece_object_list
    piece_list = [["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"],
                  ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"],
                  ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]]
    color_list = [["black", "black", "black", "black", "black", "black", "black", "black"],
                  ["black", "black", "black", "black", "black", "black", "black", "black"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ["empty", "empty", "empty", "empty", "empty", "empty", "empty", "empty"],
                  ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white'],
                  ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']]
    pawn_moved_black = ["no", "no", "no", "no", "no", "no", "no", "no"]
    pawn_moved_white = ["no", "no", "no", "no", "no", "no", "no", "no"]
    king_moved_ = ["no", "no"]
    rook_moved_ = ["no", "no", "no", "no", "yes"]
    en_passant_list = [["no", "no", "no", "no", "no", "no", "no", "no"],
                       ["no", "no", "no", "no", "no", "no", "no", "no"]]
    piece_object_list = []
    current_move = 1
    en_passant_last = 0
    king_check_last = 0
    non_capture_moves = 0
    successful_block = False
    editor_enabled = False


def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)
    widget.bind("<ButtonRelease-1>", on_drag_release)


def make_undraggable(widget):
    widget.unbind('<Button-1>')
    widget.unbind("<B1-Motion>")
    widget.unbind("<ButtonRelease-1>")


def on_drag_start(event):
    widget = event.widget
    widget.drag_start_x = event.x
    widget.drag_start_y = event.y
    widget.initial_position_x = widget.winfo_x()
    widget.initial_position_y = widget.winfo_y()
    widget.lift()


def on_drag_motion(event):
    widget = event.widget
    x = widget.winfo_x() - widget.drag_start_x + event.x
    y = widget.winfo_y() - widget.drag_start_y + event.y
    widget.place(x=x, y=y)


def on_drag_release(event):
    global non_capture_moves
    widget = event.widget
    x = widget.winfo_x() + 30
    y = widget.winfo_y() + 30
    corner_x = round(x / 100) * 100
    corner_y = round(y / 100) * 100
    if x - corner_x > 0:
        center_x = corner_x + 50
    else:
        center_x = corner_x - 50
    if center_x < 0:
        center_x = 50
    if center_x > 800:
        center_x = 750
    if y - corner_y > 0:
        center_y = corner_y + 50
    else:
        center_y = corner_y - 50
    if center_y < 0:
        center_y = 50
    if center_y > 800:
        center_y = 750
    final_x = int(-.5 + (center_x / 100))
    final_y = int(-.5 + (center_y / 100))
    initial_x = int((widget.initial_position_x - 20) / 100)
    initial_y = int((widget.initial_position_y - 20) / 100)
    piece_moved = piece_list[initial_y][initial_x]
    color_moved = color_list[initial_y][initial_x]
    piece_taken = piece_list[final_y][final_x]
    color_taken = color_list[final_y][final_x]
    if piece_list[final_y][final_x] == 'empty':
        if determine_move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved) == "success":
            update_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved)
            if determine_king_check(piece_moved, color_moved, final_y, final_x, initial_x, 0) == 'no check':
                move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, event, center_x, center_y)
                non_capture_moves += 1
            else:
                undo_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, piece_taken, color_taken)
                color_king_red(color_moved)
                widget.place(x=widget.initial_position_x, y=widget.initial_position_y)
        else:
            widget.place(x=widget.initial_position_x, y=widget.initial_position_y)
    elif color_list[final_y][final_x] == 'black' and color_list[initial_y][initial_x] == 'white':
        if determine_move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved) == "success":
            update_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved)
            if determine_king_check(piece_moved, color_moved, final_y, final_x, initial_x, 0) == 'no check':
                move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, event, center_x, center_y)
                non_capture_moves = 0
            else:
                undo_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, piece_taken, color_taken)
                color_king_red(color_moved)
                widget.place(x=widget.initial_position_x, y=widget.initial_position_y)
        else:
            widget.place(x=widget.initial_position_x, y=widget.initial_position_y)
    elif color_list[final_y][final_x] == 'white' and color_list[initial_y][initial_x] == 'black':
        if determine_move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved) == "success":
            update_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved)
            if determine_king_check(piece_moved, color_moved, final_y, final_x, initial_x, 0) == 'no check':
                move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, event, center_x, center_y)
                non_capture_moves = 0
            else:
                undo_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, piece_taken, color_taken)
                color_king_red(color_moved)
                widget.place(x=widget.initial_position_x, y=widget.initial_position_y)
        else:
            widget.place(x=widget.initial_position_x, y=widget.initial_position_y)
    else:
        widget.place(x=widget.initial_position_x, y=widget.initial_position_y)


def update_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved):
    if piece_moved == "pawn" and final_x != initial_x and color_list[final_y][final_x] == 'empty':
        piece_list[initial_y][final_x] = 'empty'
        color_list[initial_y][final_x] = 'empty'
        for i in root.place_slaves():
            if ((i.winfo_x() - 20) / 100) == final_x and ((i.winfo_y() - 20) / 100) == initial_y:
                i.destroy()
    piece_list[initial_y][initial_x] = 'empty'
    piece_list[final_y][final_x] = piece_moved
    color_list[initial_y][initial_x] = 'empty'
    color_list[final_y][final_x] = color_moved
    if piece_moved == 'pawn' and color_moved == 'black':
        if final_y == 7:
            piece_list[7][final_x] = 'queen'
            color_list[7][final_x] = 'black'
    if piece_moved == 'pawn' and color_moved == 'white':
        if final_y == 0:
            piece_list[0][final_x] = 'queen'
            color_list[0][final_x] = 'white'
    if piece_moved == "king" and final_x - initial_x == 2:
        piece_list[final_y][5] = 'rook'
        color_list[final_y][5] = color_moved
        piece_list[final_y][7] = 'empty'
        color_list[final_y][7] = 'empty'
    if piece_moved == 'king' and final_x - initial_x == -2:
        piece_list[final_y][3] = 'rook'
        color_list[final_y][3] = color_moved
        piece_list[final_y][0] = 'empty'
        color_list[final_y][0] = 'empty'


def undo_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, piece_taken, color_taken):
    if piece_moved == "pawn" and final_x != initial_x and \
            en_passant_list[get_king_type(get_color_moved_opposite(color_moved))][final_x] == 'yes' \
            and get_en_passant_y(color_moved) == final_y:
        piece_list[initial_y][final_x] = 'pawn'
        color_list[initial_y][final_x] = get_color_moved_opposite(color_moved)
        if color_moved == 'black':
            pawn = Button(root, image=w_pawn, bg=piece_bg_white, cursor='cross')
            pawn.place(x=(final_x * 100) + 20, y=(initial_y * 100) + 20)
        if color_moved == 'white':
            pawn = Button(root, image=b_pawn, bg=piece_bg_black, cursor='cross')
            pawn.place(x=(final_x * 100) + 20, y=(initial_y * 100) + 20)
    piece_list[initial_y][initial_x] = piece_moved
    piece_list[final_y][final_x] = piece_taken
    color_list[initial_y][initial_x] = color_moved
    color_list[final_y][final_x] = color_taken
    if piece_moved == 'pawn' and color_moved == 'black':
        if final_y == 7:
            piece_list[7][final_x] = 'empty'
            color_list[7][final_x] = 'empty'
    if piece_moved == 'pawn' and color_moved == 'white':
        if final_y == 0:
            piece_list[0][final_x] = 'empty'
            color_list[0][final_x] = 'empty'
    if piece_moved == "king" and final_x - initial_x == 2:
        piece_list[final_y][5] = 'empty'
        color_list[final_y][5] = 'empty'
        piece_list[final_y][7] = 'rook'
        color_list[final_y][7] = color_moved
    if piece_moved == 'king' and final_x - initial_x == -2:
        piece_list[final_y][3] = 'empty'
        color_list[final_y][3] = 'empty'
        piece_list[final_y][0] = 'rook'
        color_list[final_y][0] = color_moved


def move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, event, center_x, center_y):
    if event != 'PGN':
        widget = event.widget
        widget.place(x=center_x - 30, y=center_y - 30)
    # else:
    #    for i in root.place_slaves():
    #       if ((i.winfo_x() - 20) / 100) == initial_x and ((i.winfo_y() - 20) / 100) == initial_y:
    #          widget = i
    #         widget.place(x=center_x - 30, y=center_y - 30)
    update_array(final_x, final_y, initial_y, initial_x, piece_moved, color_moved)
    global en_passant_last
    global en_passant_list
    if piece_moved == 'pawn' and np.abs(final_y - initial_y) == 2:
        if color_moved == 'white':
            en_passant_list[0][final_x] = "yes"
        if color_moved == 'black':
            en_passant_list[1][final_x] = 'yes'
        en_passant_last = 1
    else:
        en_passant_last = 0
        en_passant_list = [["no", "no", "no", "no", "no", "no", "no", "no"],
                           ["no", "no", "no", "no", "no", "no", "no", "no"]]
    if piece_moved == 'pawn' and color_moved == 'black':
        if initial_y == 6:
            pawn_moved_black[initial_x] = 'yes'
        if final_y == 7:
            widget.destroy()
            queen = Button(root, image=b_queen, bg=piece_bg_black, cursor='cross')
            queen.place(x=(final_x * 100) + 20, y=(final_y * 100) + 20)
            make_draggable(queen)
    if piece_moved == 'pawn' and color_moved == 'white':
        if initial_y == 1:
            pawn_moved_white[initial_x] = 'yes'
        if final_y == 0:
            widget.destroy()
            queen = Button(root, image=w_queen, bg=piece_bg_white, cursor='cross')
            queen.place(x=(final_x * 100) + 20, y=(final_y * 100) + 20)
            make_draggable(queen)
    if piece_moved == "king" and final_x - initial_x == 2:
        if color_moved == 'white':
            rook = Button(root, bg=piece_bg_white, image=w_rook, cursor='cross')
            rook.place(x=(5 * 100) + 20, y=(7 * 100) + 20)
            make_draggable(rook)
        if color_moved == 'black':
            rook = Button(root, bg=piece_bg_black, image=b_rook, cursor='cross')
            rook.place(x=(5 * 100) + 20, y=(0 * 100) + 20)
            make_draggable(rook)
        for i in root.place_slaves():
            if ((i.winfo_x() - 20) / 100) == 7 and ((i.winfo_y() - 20) / 100) == final_y:
                i.destroy()
    if piece_moved == 'king' and final_x - initial_x == -2:
        if color_moved == 'white':
            rook = Button(root, bg=piece_bg_white, image=w_rook, cursor='cross')
            rook.place(x=(3 * 100) + 20, y=(7 * 100) + 20)
            make_draggable(rook)
        if color_moved == 'black':
            rook = Button(root, bg=piece_bg_black, image=b_rook, cursor='cross')
            rook.place(x=(3 * 100) + 20, y=(0 * 100) + 20)
            make_draggable(rook)
        for i in root.place_slaves():
            if ((i.winfo_x() - 20) / 100) == 0 and ((i.winfo_y() - 20) / 100) == final_y:
                i.destroy()
    if piece_moved == "king":
        king_moved_[get_king_type(color_moved)] = "yes"
    if piece_moved == "rook":
        rook_moved_[get_rook_type(color_moved, final_y)] = 'yes'
    global king_check_last
    if king_check_last == 1:
        king_check_last = 0
        color_king_default(color_moved)
    if event != 'PGN':
        for i in root.place_slaves():
            if ((i.winfo_x() - 20) / 100) == final_x and ((i.winfo_y() - 20) / 100) == final_y:
                i.destroy()
        global current_move
        if current_move % 2 != 0:
            for i in root.place_slaves():
                if i.cget("bg") == piece_bg_white:
                    make_undraggable(i)
                if i.cget("bg") == piece_bg_black:
                    make_draggable(i)
        if current_move % 2 == 0:
            for i in root.place_slaves():
                if i.cget("bg") == piece_bg_white:
                    make_draggable(i)
                if i.cget("bg") == piece_bg_black:
                    make_undraggable(i)
        current_move += 1
    if event != "PGN":
        if determine_king_check(piece_moved, color_moved, final_y, final_x, initial_x, 1) != 'no check':
            color_king_red(color_moved, 1)
            if determine_checkmate(piece_moved, color_moved, final_y, final_x) == 'checkmate':
                color_moved_display = 'bug'
                if color_moved == 'white':
                    color_moved_display = 'White'
                if color_moved == 'black':
                    color_moved_display = 'Black'
                checkmate_box = messagebox.askyesno("Checkmate",
                                                    "Checkmate. %s wins.\nReset Board?" % color_moved_display)
                if checkmate_box:
                    reset_board()
        if determine_stalemate(piece_moved, color_moved, final_y, final_x) == 'stalemate':
            color_moved_display = 'bug'
            if color_moved == 'white':
                color_moved_display = 'Black'
            if color_moved == 'black':
                color_moved_display = 'White'
            stalemate_box = messagebox.askyesno("Stalemate", "Stalemate.\n%s has no legal moves.\nReset Board?" %
                                                color_moved_display)
            if stalemate_box:
                reset_board()
        if determine_draw() == 'insufficient':
            draw_box = messagebox.askyesno("Draw", "Draw by insufficient material.\nReset Board?")
            if draw_box:
                reset_board()
        if determine_draw() == '50_move':
            draw_box = messagebox.askyesno("Draw", "Draw by 50 move rule.\nReset Board?")
            if draw_box:
                reset_board()


def get_king_type(color):
    if color == 'white':
        return 0
    if color == 'black':
        return 1


def get_rook_type(color, final_y):
    if color == 'white':
        if final_y > 3:
            return 0
        else:
            return 1
    if color == "black":
        if final_y < 3:
            return 2
        else:
            return 3
    else:
        return 5


def get_en_passant_y(color_moved):
    if color_moved == 'black':
        return 5
    if color_moved == 'white':
        return 2


def get_color_bg(color):
    if color == 'white':
        return piece_bg_white
    if color == 'black':
        return piece_bg_black


def get_color_moved_opposite(color_moved, stage=0):
    if stage == 1 or stage == 2:
        return color_moved
    if color_moved == 'white':
        return 'black'
    else:
        return 'white'


def get_king_position(color_moved, stage=0):
    if stage == 1 or stage == 2:
        color_moved = get_color_moved_opposite(color_moved)
    for i in root.place_slaves():
        if i.winfo_y() < 800:
            if color_moved == 'white':
                if i.cget("image") == "pyimage3":
                    return i.winfo_x() - 20, i.winfo_y() - 20
            if color_moved == 'black':
                if i.cget('image') == "pyimage4":
                    return i.winfo_x() - 20, i.winfo_y() - 20


def color_king_red(color_moved, stage=0):
    global king_check_last
    king_check_last = 1
    if stage == 1 or stage == 2:
        color_moved = get_color_moved_opposite(color_moved)
    for i in root.place_slaves():
        if i.winfo_y() < 800:
            if color_moved == 'white':
                if i.cget("image") == "pyimage3":
                    i.config(bg='red')
            if color_moved == 'black':
                if i.cget("image") == "pyimage4":
                    i.config(bg='red')


def color_king_default(color_moved):
    for i in root.place_slaves():
        if i.winfo_y() < 800:
            if color_moved == 'white':
                if i.cget("image") == "pyimage3":
                    i.config(bg=piece_bg_white)
            if color_moved == 'black':
                if i.cget("image") == "pyimage4":
                    i.config(bg=piece_bg_black)


def determine_checkmate(piece_moved, color_moved, final_y, final_x, stage=1):
    king_x, king_y = get_king_position(color_moved, 1)
    king_x = int(king_x / 100)
    king_y = int(king_y / 100)
    color_moved_opposite = get_color_moved_opposite(color_moved)

    # Check all king moves, if 0 then it is checkmate.
    king_moves = 8
    if king_y != 7 and king_y != 0 and king_x != 7 and king_x != 0:
        king_moves = 8
    elif king_y == 7 or king_y == 0:
        if king_x == 7 or king_x == 0:
            king_moves = 3
        else:
            king_moves = 5
    elif king_x == 7 or king_x == 0:
        if king_y == 7 or king_y == 0:
            king_moves = 3
        else:
            king_moves = 5
    for i in range(3):
        for j in range(3):
            if 0 <= king_y + (i - 1) <= 7 and 0 <= king_x + (j - 1) <= 7:
                if (i - 1) == 0 and (j - 1) == 0:
                    pass
                else:
                    if color_list[king_y + (i - 1)][king_x + (j - 1)] == color_moved_opposite:
                        king_moves -= 1
                    elif determine_king_check(piece_moved, color_moved, king_y + (i - 1), king_x + (j - 1),
                                              -10, 2) != 'no check':
                        if stage != 2:
                            attacking_piece, attacking_y, attacking_x = determine_king_check(piece_moved, color_moved,
                                                                                             king_y + (i - 1),
                                                                                             king_x + (j - 1),
                                                                                             -10, 1)
                            attacking_king_piece, attacking_king_y, attacking_king_x = determine_king_check(piece_moved,
                                                                                                            color_moved,
                                                                                                            king_y,
                                                                                                            king_x,
                                                                                                            -10, 1)
                            if attacking_piece == attacking_king_piece and attacking_y == attacking_king_y and \
                                    attacking_x == attacking_king_x:
                                final_y = attacking_y
                                final_x = attacking_x
                                piece_moved = attacking_piece
                        king_moves -= 1
    if king_moves == 0:
        global successful_block
        successful_block = False
        for k in root.place_slaves():
            if k.cget("bg") == get_color_bg(color_moved_opposite):
                k_piece_y = int((k.winfo_y() + 20) / 100)
                k_piece_x = int((k.winfo_x() + 20) / 100)
                k_piece_moved = ""
                if k.cget("image") == "pyimage11" or k.cget("image") == "pyimage12":
                    k_piece_moved = 'pawn'
                if k.cget("image") == "pyimage7" or k.cget("image") == "pyimage8":
                    k_piece_moved = 'knight'
                if k.cget("image") == "pyimage9" or k.cget("image") == "pyimage10":
                    k_piece_moved = 'bishop'
                if k.cget("image") == "pyimage6" or k.cget("image") == "pyimage5":
                    k_piece_moved = "queen"
                if k.cget("image") == "pyimage3" or k.cget("image") == "pyimage4":
                    k_piece_moved = "skip"
                if k.cget("image") == "pyimage1" or k.cget("image") == "pyimage2":
                    k_piece_moved = "rook"
                if piece_moved == "queen" or piece_moved == "rook":
                    if king_x - final_x > 0 and king_y == final_y:
                        for m in range(king_x - final_x):
                            if determine_move_piece(king_x - (m + 1), king_y, k_piece_y, k_piece_x, k_piece_moved,
                                                    color_moved_opposite) == "success":
                                successful_block = True
                    if king_x - final_x < 0 and king_y == final_y:
                        for m in range(final_x - king_x):
                            if determine_move_piece(king_x + (m + 1), king_y, k_piece_y, k_piece_x, k_piece_moved,
                                                    color_moved_opposite) == "success":
                                successful_block = True
                    if king_y - final_y > 0 and king_x == final_x:
                        for m in range(king_y - final_y):
                            if determine_move_piece(king_x, king_y - (m + 1), k_piece_y, k_piece_x, k_piece_moved,
                                                    color_moved_opposite) == "success":
                                successful_block = True
                    if king_y - final_y < 0 and king_x == final_x:
                        for m in range(final_y - king_y):
                            if determine_move_piece(king_x, king_y + (m + 1), k_piece_y, k_piece_x, k_piece_moved,
                                                    color_moved_opposite) == "success":
                                successful_block = True
                if piece_moved == "bishop" or piece_moved == 'queen':
                    if king_x > final_x:
                        for n in [-1, 1]:
                            for m in range(king_x - final_x):
                                if 0 <= king_x - (m + 1) <= 7 and 0 <= king_y + (n * (m + 1)) <= 7:
                                    if determine_move_piece(king_x - (m + 1), king_y + (n * (m + 1)), k_piece_y,
                                                            k_piece_x,
                                                            k_piece_moved, color_moved_opposite) == 'success':
                                        successful_block = True
                    if king_x < final_x:
                        for n in [-1, 1]:
                            for m in range(final_x - king_x):
                                if 0 <= king_x - (m + 1) <= 7 and 0 <= king_y + (n * (m + 1)) <= 7:
                                    if determine_move_piece(king_x + (m + 1), king_y + (n * (m + 1)), k_piece_y,
                                                            k_piece_x,
                                                            k_piece_moved, color_moved_opposite) == 'success':
                                        successful_block = True
                if piece_moved == "knight":
                    successful_block = False
                if piece_moved == "pawn":
                    successful_block = False
        if not successful_block:
            return "checkmate"


def determine_stalemate(piece_moved, color_moved, final_y, final_x):
    if determine_checkmate(piece_moved, color_moved, final_y, final_x, 2) == 'checkmate':
        loop_must_break = False
        piece_could_move = False
        y = -1
        for i in color_list:
            y += 1
            x = -1
            for j in i:
                x += 1
                if j == get_color_moved_opposite(color_moved):
                    for m in range(8):
                        for n in range(8):
                            if determine_move_piece(n, m, y, x, piece_list[m][n],
                                                    get_color_moved_opposite(color_moved)) == 'success':
                                piece_could_move = True
                                loop_must_break = True
                        if loop_must_break:
                            break
                if loop_must_break:
                    break
            if loop_must_break:
                break
        if not piece_could_move:
            return "stalemate"


def determine_draw():
    global non_capture_moves
    loop_must_break = False
    for i in piece_list:
        for j in i:
            if j != 'king' and j != 'empty':
                loop_must_break = True
                break
        if loop_must_break:
            break
    if not loop_must_break:
        return "insufficient"
    black_knight_sum = 0
    white_knight_sum = 0
    black_bishop_sum = 0
    white_bishop_sum = 0
    dark_black_bishop_sum = 0
    light_black_bishop_sum = 0
    dark_white_bishop_sum = 0
    light_white_bishop_sum = 0
    loop_must_break = False
    insufficient = True
    y = -1
    for i in piece_list:
        y += 1
        x = -1
        for j in i:
            x += 1
            if j != 'knight' and j != 'bishop' and j != 'king' and j != 'empty':
                loop_must_break = True
                break
            else:
                if j == 'knight' and color_list[y][x] == 'black':
                    black_knight_sum += 1
                if j == 'knight' and color_list[y][x] == 'white':
                    white_knight_sum += 1
                if j == 'bishop' and color_list[y][x] == 'black':
                    black_bishop_sum += 1
                    if ((y * 8) + x) % 2 == 0:
                        dark_black_bishop_sum += 1
                    else:
                        light_black_bishop_sum += 1
                if j == 'bishop' and color_list[y][x] == 'white':
                    white_bishop_sum += 1
                    if ((y * 8) + x) % 2 == 0:
                        dark_white_bishop_sum += 1
                    else:
                        light_white_bishop_sum += 1
        if loop_must_break:
            break
    if not loop_must_break:
        if white_knight_sum > 1:
            insufficient = False
        if black_knight_sum > 1:
            insufficient = False
        if not insufficient:
            if white_bishop_sum > 1:
                if dark_white_bishop_sum > 1 or light_white_bishop_sum > 1:
                    pass
                else:
                    stalemate = False
            if black_bishop_sum > 1:
                if dark_black_bishop_sum > 1 or light_black_bishop_sum > 1:
                    pass
                else:
                    stalemate = False
        if not insufficient:
            if white_bishop_sum > 0 and black_bishop_sum > 0:
                insufficient = False
            if white_knight_sum > 0 and black_knight_sum > 0:
                insufficient = False
        if not insufficient:
            if white_bishop_sum == 1 and white_knight_sum == 1:
                insufficient = False
            if black_bishop_sum == 1 and black_knight_sum == 1:
                insufficient = False
        if not insufficient:
            if white_knight_sum != black_knight_sum:
                return "insufficient"
        if insufficient:
            return "insufficient"
    if non_capture_moves == 50:
        return "50_move"


def determine_king_check(piece_moved, color_moved, final_y, final_x, initial_x, stage):
    if piece_moved == 'king' and stage != 1:
        king_x = final_x
        king_y = final_y
    elif stage == 2:
        king_x = final_x
        king_y = final_y
    else:
        king_x, king_y = get_king_position(color_moved, stage)
        king_x = int(king_x / 100)
        king_y = int(king_y / 100)
    color_moved_opposite = get_color_moved_opposite(color_moved, stage)
    if stage == 1 or stage == 2:
        color_moved = get_color_moved_opposite(color_moved)
    for i in range(7 - king_y):
        if color_list[(i + 1) + king_y][king_x] == color_moved:
            if stage != 2:
                break
            elif piece_list[(i + 1) + king_y][king_x] != 'king':
                break
        if piece_list[(i + 1) + king_y][king_x] != "rook" and piece_list[(i + 1) + king_y][king_x] != "queen" and \
                piece_list[(i + 1) + king_y][king_x] != 'empty':
            if stage != 2:
                break
            elif piece_list[(i + 1) + king_y][king_x] != 'king':
                break
        if piece_list[(i + 1) + king_y][king_x] == 'queen' or piece_list[(i + 1) + king_y][king_x] == 'rook':
            if color_list[(i + 1) + king_y][king_x] == color_moved_opposite:
                return piece_list[(i + 1) + king_y][king_x], (i + 1) + king_y, king_x
    for i in range(king_y):
        if color_list[-(i + 1) + king_y][king_x] == color_moved:
            if color_list[-(i + 1) + king_y][king_x] == color_moved:
                if stage != 2:
                    break
                elif piece_list[-(i + 1) + king_y][king_x] != 'king':
                    break
        if piece_list[-(i + 1) + king_y][king_x] != "rook" and piece_list[-(i + 1) + king_y][king_x] != "queen" and \
                piece_list[-(i + 1) + king_y][king_x] != 'empty':
            if stage != 2:
                break
            elif piece_list[-(i + 1) + king_y][king_x] != 'king':
                break
        if piece_list[-(i + 1) + king_y][king_x] == 'queen' or piece_list[-(i + 1) + king_y][king_x] == 'rook':
            if color_list[-(i + 1) + king_y][king_x] == color_moved_opposite:
                return piece_list[-(i + 1) + king_y][king_x], -(i + 1) + king_y, king_x
    for i in range(7 - king_x):
        if color_list[king_y][(i + 1) + king_x] == color_moved:
            if color_list[king_y][(i + 1) + king_x] == color_moved:
                if stage != 2:
                    break
                elif piece_list[king_y][(i + 1) + king_x] != 'king':
                    break
        if piece_list[king_y][(i + 1) + king_x] != "rook" and piece_list[king_y][(i + 1) + king_x] != "queen" and \
                piece_list[king_y][(i + 1) + king_x] != 'empty':
            if stage != 2:
                break
            elif piece_list[king_y][(i + 1) + king_x] != 'king':
                break
        if piece_list[king_y][(i + 1) + king_x] == 'queen' or piece_list[king_y][(i + 1) + king_x] == 'rook':
            if color_list[king_y][(i + 1) + king_x] == color_moved_opposite:
                return piece_list[king_y][(i + 1) + king_x], king_y, (i + 1) + king_x
    for i in range(king_x):
        if color_list[king_y][-(i + 1) + king_x] == color_moved:
            if color_list[king_y][-(i + 1) + king_x] == color_moved:
                if stage != 2:
                    break
                elif piece_list[king_y][-(i + 1) + king_x] != 'king':
                    break
        if piece_list[king_y][-(i + 1) + king_x] != "rook" and piece_list[king_y][-(i + 1) + king_x] != "queen" and \
                piece_list[king_y][-(i + 1) + king_x] != 'empty':
            if stage != 2:
                break
            elif piece_list[king_y][-(i + 1) + king_x] != 'king':
                break
        if piece_list[king_y][-(i + 1) + king_x] == 'queen' or piece_list[king_y][-(i + 1) + king_x] == 'rook':
            if color_list[king_y][-(i + 1) + king_x] == color_moved_opposite:
                return piece_list[king_y][-(i + 1) + king_x], king_y, -(i + 1) + king_x
    for j in [-1, 1]:
        for i in range(king_x):
            if 7 >= king_y - (j * (i + 1)) >= 0:
                if color_list[king_y - (j * (i + 1))][king_x - (i + 1)] == color_moved:
                    if stage != 2:
                        break
                    elif piece_list[king_y - (j * (i + 1))][king_x - (i + 1)] != 'king':
                        break
                if piece_list[king_y - (j * (i + 1))][king_x - (i + 1)] != 'queen' and \
                        piece_list[king_y - (j * (i + 1))][king_x - (i + 1)] != 'bishop' and \
                        piece_list[king_y - (j * (i + 1))][king_x - (i + 1)] != 'empty':
                    if stage != 2:
                        break
                    elif piece_list[king_y - (j * (i + 1))][king_x - (i + 1)] != 'king':
                        break
                if piece_list[king_y - (j * (i + 1))][king_x - (i + 1)] == 'queen' or \
                        piece_list[king_y - (j * (i + 1))][
                            king_x - (i + 1)] == 'bishop':
                    if color_list[king_y - (j * (i + 1))][king_x - (i + 1)] == color_moved_opposite:
                        return piece_list[king_y - (j * (i + 1))][king_x - (i + 1)], king_y - (j * (i + 1)), king_x - (
                                i + 1)
    for j in [-1, 1]:
        for i in range(7 - king_x):
            if 0 <= king_y + (j * (i + 1)) <= 7:
                if color_list[king_y + (j * (i + 1))][king_x + (i + 1)] == color_moved:
                    if stage != 2:
                        break
                    elif piece_list[king_y + (j * (i + 1))][king_x + (i + 1)] != 'king':
                        break
                if piece_list[king_y + (j * (i + 1))][king_x + (i + 1)] != 'queen' and \
                        piece_list[king_y + (j * (i + 1))][king_x + (i + 1)] != 'bishop' and \
                        piece_list[king_y + (j * (i + 1))][king_x + (i + 1)] != 'empty':
                    if stage != 2:
                        break
                    elif piece_list[king_y + (j * (i + 1))][king_x + (i + 1)] != 'king':
                        break
                if piece_list[king_y + (j * (i + 1))][king_x + (i + 1)] == 'queen' or \
                        piece_list[king_y + (j * (i + 1))][
                            king_x + (i + 1)] == 'bishop':
                    if color_list[king_y + (j * (i + 1))][king_x + (i + 1)] == color_moved_opposite:
                        return piece_list[king_y + (j * (i + 1))][king_x + (i + 1)], king_y + (j * (i + 1)), king_x + (
                                i + 1)
    for i in [-1, 1]:
        if 7 >= king_y + (i * 1) >= 0 and 7 >= king_x + (i * 2) >= 0:
            if piece_list[king_y + (i * 1)][king_x + (i * 2)] == 'knight':
                if color_list[king_y + (i * 1)][king_x + (i * 2)] == color_moved_opposite:
                    return piece_list[king_y + (i * 1)][king_x + (i * 2)], king_y + (i * 1), king_x + (i * 2)
        if 7 >= king_y + (i * 2) >= 0 and 7 >= king_x - (i * 1) >= 0:
            if piece_list[king_y + (i * 2)][king_x - (i * 1)] == 'knight':
                if color_list[king_y + (i * 2)][king_x - (i * 1)] == color_moved_opposite:
                    return piece_list[king_y + (i * 2)][king_x - (i * 1)], king_y + (i * 2), king_x - (i * 1)
        if 7 >= king_y - (i * 2) >= 0 and 7 >= king_x - (i * 1) >= 0:
            if piece_list[king_y - (i * 2)][king_x - (i * 1)] == 'knight':
                if color_list[king_y - (i * 2)][king_x - (i * 1)] == color_moved_opposite:
                    return piece_list[king_y - (i * 2)][king_x - (i * 1)], king_y - (i * 2), king_x - (i * 1)
        if 7 >= king_y - (i * 1) >= 0 and 7 >= king_x + (i * 2) >= 0:
            if piece_list[king_y - (i * 1)][king_x + (i * 2)] == 'knight':
                if color_list[king_y - (i * 1)][king_x + (i * 2)] == color_moved_opposite:
                    return piece_list[king_y - (i * 1)][king_x + (i * 2)], king_y - (i * 1), king_x + (i * 2)
    if 0 <= king_x + 1 <= 7 and 0 <= king_y + 1 <= 7:
        if piece_list[king_y + 1][king_x + 1] == 'pawn':
            if color_moved == 'black' and color_list[king_y + 1][king_x + 1] == color_moved_opposite:
                return piece_list[king_y + 1][king_x + 1], king_y + 1, king_x + 1
    if 0 <= king_x - 1 <= 7 and 0 <= king_y + 1 <= 7:
        if piece_list[king_y + 1][king_x - 1] == 'pawn':
            if color_moved == 'black' and color_list[king_y + 1][king_x - 1] == color_moved_opposite:
                return piece_list[king_y + 1][king_x - 1], king_y + 1, king_x - 1
    if 0 <= king_x + 1 <= 7 and 0 <= king_y - 1 <= 7:
        if piece_list[king_y - 1][king_x + 1] == 'pawn':
            if color_moved == 'white' and color_list[king_y - 1][king_x + 1] == color_moved_opposite:
                return piece_list[king_y - 1][king_x + 1], king_y - 1, king_x + 1
    if 0 <= king_x - 1 <= 7 and 0 <= king_y - 1 <= 7:
        if piece_list[king_y - 1][king_x - 1] == 'pawn':
            if color_moved == 'white' and color_list[king_y - 1][king_x - 1] == color_moved_opposite:
                return piece_list[king_y - 1][king_x - 1], king_y - 1, king_x - 1
    for i in range(3):
        for j in range(3):
            if 0 <= king_y + (i - 1) <= 7 and 0 <= king_x + (j - 1) <= 7:
                if i == 0 and j == 0:
                    pass
                else:
                    if piece_list[king_y + (i - 1)][king_x + (j - 1)] == "king":
                        if color_list[king_y + (i - 1)][king_x + (j - 1)] == color_moved_opposite:
                            return piece_list[king_y + (i - 1)][king_x + (j - 1)], king_y + (i - 1), king_x + (j - 1)
    if piece_moved == 'king' and np.abs(final_x - initial_x) == 2 and stage == 0:
        if final_x - initial_x > 0:
            if determine_king_check(piece_moved, color_moved, final_y, final_x - 1, -10, 0) != 'no check' or \
                    determine_king_check(piece_moved, color_moved, final_y, final_x - 2, -10, 0) != 'no check':
                return piece_list[final_y][final_x - 1], king_y, king_x
        if final_x - initial_x < 0:
            if determine_king_check(piece_moved, color_moved, final_y, final_x + 1, -10, 0) != 'no check' or \
                    determine_king_check(piece_moved, color_moved, final_y, final_x + 2, -10, 0) != 'no check':
                return piece_list[final_y][final_x + 1], king_y, king_x
    return 'no check'


def determine_move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved):
    if piece_moved == "king":
        if np.abs(initial_x - final_x) <= 1 and np.abs(initial_y - final_y) <= 1:
            return "success"
    if piece_moved == "king" and final_x - initial_x == 2 and king_moved_[get_king_type(color_moved)] == 'no' and \
            piece_list[final_y][7] == 'rook' and rook_moved_[get_rook_type(color_moved, final_y)] == "no":
        if piece_list[final_y][5] == 'empty' and piece_list[final_y][6] == 'empty' and king_check_last == 0:
            return "success"
    if piece_moved == "king" and final_x - initial_x == -2 and king_moved_[get_king_type(color_moved)] == 'no' and \
            piece_list[final_y][0] == 'rook' and rook_moved_[get_rook_type(color_moved, final_y)] == "no":
        if piece_list[final_y][1] == 'empty' and piece_list[final_y][2] == 'empty' and piece_list[final_y][3] \
                == 'empty' and king_check_last == 0:
            return "success"
    if piece_moved == "pawn" and final_x == initial_x and color_list[final_y][final_x] == 'empty':
        if final_y - initial_y == 1 and color_moved == 'black':
            return "success"
        elif initial_y - final_y == 1 and color_moved == 'white':
            return "success"
        elif final_y - initial_y == 2 and initial_y == 1 and color_moved == 'black' and pawn_moved_black[initial_x] \
                == "no":
            return "success"
        elif initial_y - final_y == 2 and initial_y == 6 and color_moved == 'white' and pawn_moved_white[initial_x] \
                == "no":
            return "success"
    if piece_moved == "pawn" and final_x != initial_x and color_list[final_y][final_x] != 'empty':
        if np.abs(final_x - initial_x) == 1 and final_y - initial_y == 1 and color_moved == 'black':
            return "success"
        if np.abs(final_x - initial_x) == 1 and initial_y - final_y == 1 and color_moved == 'white':
            return "success"
    if piece_moved == "pawn" and final_x != initial_x and color_list[final_y][final_x] == 'empty':
        if np.abs(final_x - initial_x) == 1 and final_y - initial_y == 1 and color_moved == 'black' and en_passant_last \
                == 1 and final_y == 5:
            if en_passant_list[0][final_x] == "yes":
                return "success"
        if np.abs(final_x - initial_x) == 1 and initial_y - final_y == 1 and color_moved == 'white' and en_passant_last \
                == 1 and final_y == 2:
            if en_passant_list[1][final_x] == "yes":
                return "success"
    if piece_moved == "rook" or piece_moved == "queen":
        if final_y == initial_y:
            x_distance = np.abs(final_x - initial_x)
            if final_x - initial_x > 0:
                direction = 1
            else:
                direction = -1
            collision = False
            for i in range(x_distance - 1):
                if piece_list[initial_y][((i + 1) * direction) + initial_x] != 'empty':
                    collision = True
            if not collision:
                return "success"
        if final_x == initial_x:
            y_distance = np.abs(final_y - initial_y)
            if final_y - initial_y > 0:
                direction = 1
            else:
                direction = -1
            collision = False
            for i in range(y_distance - 1):
                if piece_list[((i + 1) * direction) + initial_y][initial_x] != 'empty':
                    collision = True
            if not collision:
                return "success"
    if piece_moved == "knight":
        if np.abs(final_x - initial_x) == 1 and np.abs(final_y - initial_y) == 2:
            return "success"
        if np.abs(final_x - initial_x) == 2 and np.abs(final_y - initial_y) == 1:
            return "success"
    if piece_moved == "bishop" or piece_moved == "queen":
        if np.abs(final_x - initial_x) == np.abs(final_y - initial_y):
            x_distance = np.abs(final_x - initial_x)
            if final_y - initial_y < 0:
                direction = -1
            else:
                direction = 1
            collision = False
            if final_x - initial_x < 0:
                for i in range(x_distance - 1):
                    if piece_list[((i + 1) * direction) + initial_y][((i + 1) * -1) + initial_x] != 'empty':
                        collision = True
                if not collision:
                    return "success"
            if final_x - initial_x > 0:
                for i in range(x_distance - 1):
                    if piece_list[((i + 1) * direction) + initial_y][(i + 1) + initial_x] != 'empty':
                        collision = True
                if not collision:
                    return "success"


def setup_board():
    for x in range(8):
        for y in range(8):
            if x % 2 == 0:
                if y % 2 == 0:
                    canvas.create_rectangle(x * 100, y * 100, (x + 1) * 100, (y + 1) * 100, fill=board_color_light)
                else:
                    canvas.create_rectangle(x * 100, y * 100, (x + 1) * 100, (y + 1) * 100, fill=board_color_dark)
            else:
                if y % 2 == 0:
                    canvas.create_rectangle(x * 100, y * 100, (x + 1) * 100, (y + 1) * 100, fill=board_color_dark)
                else:
                    canvas.create_rectangle(x * 100, y * 100, (x + 1) * 100, (y + 1) * 100, fill=board_color_light)
            if x == 0:
                # canvas.create_text(((x + 1) * 100) - 9, (y * 100) + 12, text=y, fill="#981b9a", font=font_style)
                canvas.create_text((x * 100) + 9, (y * 100) + 12, text=(8 - y), font=font_style)
            # if y == 0:
            #    canvas.create_text(((x + 1) * 100) - 9, (y * 100) + 12, text=x, fill="#981b9a", font=font_style)
            if y == 7:
                canvas.create_text(((x + 1) * 100) - 9, ((y + 1) * 100) - 12, text=chr(ord('@') + x + 1),
                                   font=font_style)

            if x == 0 or x == 7:
                if y == 0:
                    place_rook(x, y, 'black')
                if y == 7:
                    place_rook(x, y, 'white')
            if x == 4:
                if y == 0:
                    place_king(x, y, 'black')
                if y == 7:
                    place_king(x, y, 'white')
            if x == 1 or x == 6:
                if y == 0:
                    place_knight(x, y, 'black')
                if y == 7:
                    place_knight(x, y, 'white')
            if x == 2 or x == 5:
                if y == 0:
                    place_bishop(x, y, 'black')
                if y == 7:
                    place_bishop(x, y, 'white')
            if x == 3:
                if y == 0:
                    place_queen(x, y, 'black')
                if y == 7:
                    place_queen(x, y, 'white')
            if y == 1:
                place_pawn(x, y, 'black')
            if y == 6:
                place_pawn(x, y, 'white')

    reset_button = Button(root, bg='#16d3ca', image=pixelVirtual, text="Reset Board", width=195, height=91,
                          compound="c", font=font_style, command=reset_board)
    reset_button.place(x=801, y=2)
    enable_editor_button = Button(root, bg='orange', image=pixelVirtual, text="PGN Editor", width=94, height=92,
                                  compound="c", font=font_style, command=enable_editor)
    enable_editor_button.place(x=801, y=101)
    debug_button = Button(root, bg='darkgrey', image=pixelVirtual, text="Debug", width=94, height=92,
                          compound="c", font=font_style, command=debugger)
    debug_button.place(x=902, y=101)
    for i in root.place_slaves():
        if i.cget("bg") == piece_bg_black:
            make_undraggable(i)


def place_pawn(x, y, color):
    if color == 'black':
        pawn = Button(root, image=b_pawn, bg=piece_bg_black, cursor='cross')
    else:
        pawn = Button(root, image=w_pawn, bg=piece_bg_white, cursor='cross')
    pawn.place(x=(x * 100) + 20, y=(y * 100) + 20)
    make_draggable(pawn)
    pawn.final_x = x
    pawn.final_y = y
    piece_object_list.append(pawn)


def place_king(x, y, color):
    if color == 'black':
        king = Button(root, image=b_king, bg=piece_bg_black, cursor='cross')
    else:
        king = Button(root, image=w_king, bg=piece_bg_white, cursor='cross')
    king.place(x=(x * 100) + 20, y=(y * 100) + 20)
    make_draggable(king)
    king.final_x = x
    king.final_y = y
    piece_object_list.append(king)


def place_queen(x, y, color):
    if color == 'black':
        queen = Button(root, image=b_queen, bg=piece_bg_black, cursor='cross')
    else:
        queen = Button(root, image=w_queen, bg=piece_bg_white, cursor='cross')
    queen.place(x=(x * 100) + 20, y=(y * 100) + 20)
    make_draggable(queen)
    queen.final_x = x
    queen.final_y = y
    piece_object_list.append(queen)


def place_rook(x, y, color):
    if color == 'black':
        rook = Button(root, bg=piece_bg_black, image=b_rook, cursor='cross')
    else:
        rook = Button(root, bg=piece_bg_white, image=w_rook, cursor='cross')
    rook.place(x=(x * 100) + 20, y=(y * 100) + 20)
    make_draggable(rook)
    rook.final_x = x
    rook.final_y = y
    piece_object_list.append(rook)


def place_bishop(x, y, color):
    if color == 'black':
        bishop = Button(root, image=b_bishop, bg=piece_bg_black, cursor='cross')
    else:
        bishop = Button(root, image=w_bishop, bg=piece_bg_white, cursor='cross')
    bishop.place(x=(x * 100) + 20, y=(y * 100) + 20)
    make_draggable(bishop)
    bishop.final_x = x
    bishop.final_y = y
    piece_object_list.append(bishop)


def place_knight(x, y, color):
    if color == 'black':
        knight = Button(root, image=b_knight, bg=piece_bg_black, cursor='cross')
    else:
        knight = Button(root, image=w_knight, bg=piece_bg_white, cursor='cross')
    knight.place(x=(x * 100) + 20, y=(y * 100) + 20)
    make_draggable(knight)
    knight.final_x = x
    knight.final_y = y
    piece_object_list.append(knight)


def enable_editor():
    global editor_canvas
    disable_editor_button = Button(root, bg='red', image=pixelVirtual, text="Disable Editor", width=94, height=92,
                                   compound="c", font=font_style, command=disable_editor)
    disable_editor_button.place(x=801, y=101)
    root.geometry("1000x850")
    PGN = StringVar()
    PGN_entry = Entry(root, textvariable=PGN, width=131)
    PGN_entry.place(x=3, y=815)
    PGN_button = Button(root, bg='grey', text='Enter PGN', command=lambda: enter_PGN(PGN.get()))
    PGN_button.place(x=805, y=815)


def disable_editor():
    global editor_canvas
    enable_editor_button = Button(root, bg='orange', image=pixelVirtual, text="PGN Editor", width=94, height=92,
                                  compound="c", font=font_style, command=enable_editor)
    enable_editor_button.place(x=801, y=101)
    root.geometry("1000x800")


def enter_PGN(pgn):
    global current_move
    # reset_board()
    print(pgn)
    pgn_list = pgn.split()
    count = -1
    for i in pgn_list:
        count += 1
        if i[0].isnumeric():
            pgn_list.pop(count)
    count = -1
    for i in pgn_list:
        count += 1
        if i[1] == 'x':
            i = i.replace('x', '', 1)
            pgn_list[count] = i
        if len(i) > 2:
            if i[2] == 'x':
                i = i.replace('x', '', 1)
                pgn_list[count] = i
    count = -1
    for i in pgn_list:
        count += 1
        if i[-1] == '+':
            i = i.replace('+', '', 1)
            pgn_list[count] = i
        if i[-1] == '#':
            i = i.replace('#', '', 1)
            pgn_list[count] = i
    print(pgn_list)
    for i in pgn_list:
        initial_x = 0
        initial_y = 0
        final_x = 0
        final_y = 0
        piece_moved = ''
        if current_move % 2 == 0:
            color_moved = 'black'
        else:
            color_moved = 'white'
        if i[-1].isnumeric():
            final_y = 7 - (int(i[-1]) - 1)
            final_x = ord(i[-2]) - 97
        if i[0].islower():
            piece_moved = 'pawn'
            initial_x = ord(i[0]) - 97
            if len(i) == 3:
                if color_moved == 'white':
                    initial_y = final_y + 1
                else:
                    initial_y = final_y - 1
            else:
                if color_moved == 'white':
                    if piece_list[final_y + 1][final_x] == 'pawn':
                        initial_y = final_y + 1
                    else:
                        initial_y = final_y + 2
                else:
                    if piece_list[final_y - 1][final_x] == 'pawn':
                        initial_y = final_y - 1
                    else:
                        initial_y = final_y - 2
        if i[0] == "O":
            piece_moved = 'king'
            if color_moved == 'black':
                initial_x = 4
                initial_y = 0
                if len(i) == 3:
                    final_y = 0
                    final_x = 6
                if len(i) == 5:
                    final_y = 0
                    final_x = 1
            else:
                initial_x = 4
                initial_y = 7
                if len(i) == 3:
                    final_y = 7
                    final_x = 6
                if len(i) == 5:
                    final_y = 7
                    final_x = 1
        elif not i[0].islower():
            if i[0] == 'Q':
                piece_moved = 'queen'
            if i[0] == 'R':
                piece_moved = 'rook'
            if i[0] == 'N':
                piece_moved = 'knight'
            if i[0] == 'K':
                piece_moved = 'king'
            if i[0] == 'B':
                piece_moved = 'bishop'
            if len(i) == 3:
                y = -1
                for j in piece_list:
                    y += 1
                    x = -1
                    for k in j:
                        x += 1
                        if k == piece_moved and color_list[y][x] == color_moved:
                            initial_y_temp = y
                            initial_x_temp = x
                            if determine_move_piece(final_x, final_y, initial_y_temp, initial_x_temp, piece_moved,
                                                    color_moved) == 'success':
                                initial_y = y
                                initial_x = x
            if len(i) == 4:
                if i[1].isalpha():
                    initial_x = ord(i[1]) - 97
                    y = -1
                    for j in piece_list:
                        y += 1
                        x = -1
                        for k in j:
                            x += 1
                            if k == piece_moved and color_list[y][x] == color_moved and x == initial_x:
                                initial_y_temp = y
                                initial_x_temp = x
                                if determine_move_piece(final_x, final_y, initial_y_temp, initial_x_temp, piece_moved,
                                                        color_moved) == 'success':
                                    initial_y = y
                if i[1].isnumeric():
                    initial_y = 7 - (int(i[1]) - 1)
                    y = -1
                    for j in piece_list:
                        y += 1
                        x = -1
                        for k in j:
                            x += 1
                            if k == piece_moved and color_list[y][x] == color_moved and y == initial_y:
                                initial_y_temp = y
                                initial_x_temp = x
                                if determine_move_piece(final_x, final_y, initial_y_temp, initial_x_temp, piece_moved,
                                                        color_moved) == 'success':
                                    initial_x = x
        move_piece(final_x, final_y, initial_y, initial_x, piece_moved, color_moved, 'PGN', (final_x * 100) + 50,
                   (final_y * 100) + 50)
        current_move += 1
        for i in root.place_slaves():
            if (i.winfo_y() - 20) / 100 == initial_y and (i.winfo_x() - 20) / 100 == initial_x:
                piece_object_list.remove(i)
                i.destroy()
                for i in root.place_slaves():
                    if (i.winfo_y() - 20) / 100 == final_y and (i.winfo_x() - 20) / 100 == final_x:
                        piece_object_list.remove(i)
                        i.destroy()
                    try:
                        if i.final_y == final_y and i.final_x == final_x:
                            piece_object_list.remove(i)
                            i.destroy()
                    except:
                        pass
                if piece_moved == 'pawn':
                    place_pawn(final_x, final_y, color_moved)
                if piece_moved == 'queen':
                    place_queen(final_x, final_y, color_moved)
                if piece_moved == 'rook':
                    place_rook(final_x, final_y, color_moved)
                if piece_moved == 'bishop':
                    place_bishop(final_x, final_y, color_moved)
                if piece_moved == 'knight':
                    place_knight(final_x, final_y, color_moved)
                if piece_moved == 'king':
                    place_king(final_x, final_y, color_moved)
            try:
                if i.final_y == initial_y and i.final_x == initial_x:
                    piece_object_list.remove(i)
                    i.destroy()
                    for i in root.place_slaves():
                        if (i.winfo_y() - 20) / 100 == final_y and (i.winfo_x() - 20) / 100 == final_x:
                            piece_object_list.remove(i)
                            i.destroy()
                        try:
                            if i.final_y == final_y and i.final_x == final_x:
                                piece_object_list.remove(i)
                                i.destroy()
                        except:
                            pass
                    if piece_moved == 'pawn':
                        place_pawn(final_x, final_y, color_moved)
                    if piece_moved == 'queen':
                        place_queen(final_x, final_y, color_moved)
                    if piece_moved == 'rook':
                        place_rook(final_x, final_y, color_moved)
                    if piece_moved == 'bishop':
                        place_bishop(final_x, final_y, color_moved)
                    if piece_moved == 'knight':
                        place_knight(final_x, final_y, color_moved)
                    if piece_moved == 'king':
                        place_king(final_x, final_y, color_moved)
            except:
                pass
    piece_count = 0
    for i in root.place_slaves():
        if current_move % 2 == 0:
            if i.cget("bg") == piece_bg_white:
                make_undraggable(i)
            if i.cget("bg") == piece_bg_black:
                make_draggable(i)
        else:
            if i.cget("bg") == piece_bg_black:
                make_undraggable(i)
            if i.cget("bg") == piece_bg_white:
                make_draggable(i)
        piece_count += 1
    print("piece count=", piece_count)


def debugger():
    print(piece_list)
    print(color_list)
    print(piece_object_list)
    print(len(piece_object_list))
    for q in piece_object_list:
        print(q, q.final_y, q.final_x)
    for k in piece_list:
        for i in k:
            if i == 'pawn' or i == 'rook' or i == 'queen' or i == 'empty' or i == 'knight' or i == 'bishop' \
                    or i == 'king':
                pass
            else:
                print("Error: Invalid piece in piece_list")
    for k in color_list:
        for i in k:
            if i == 'black' or i == 'white' or i == 'empty':
                pass
            else:
                print("Error: Invalid color in color_list")


def reset_board():
    root.geometry("1000x800")
    for i in root.place_slaves():
        i.destroy()
    initialize_board()
    setup_board()


initialize_board()
setup_board()
root.mainloop()
