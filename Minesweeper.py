import tkinter as tk
import random
from tkinter import messagebox
import sys
from PIL import Image, ImageTk

TILE_SIZE = 30  # Size of each tile in pixels

def generateRandomBoard(rows, col):
    choices = ["E", "E", "E", "E", "E", "M"]
    mineCount = 0
    details = []
    board = [[] for _ in range(rows)]
    for i in range(rows):
        for _ in range(col):
            ranchar = random.choice(choices)
            if ranchar == "M":
                mineCount += 1
            board[i].append(ranchar)

    details.append(board)
    details.append(mineCount)
    return details

def numberMineBoard(board):
    vis = [["0" for _ in range(len(board[0]))] for _ in range(len(board))]
    numberOfRows = len(board)
    numberOfColumns = len(board[0])
    for i in range(0, numberOfRows):
        for j in range(0, numberOfColumns):
            if board[i][j] == "M":
                vis[i][j] = "M"
                for drow in range(-1, 2):
                    for dcol in range(-1, 2):
                        nrow = i + drow
                        ncol = j + dcol
                        if nrow >= 0 and nrow < numberOfRows and ncol >= 0 and ncol < numberOfColumns:
                            if board[nrow][ncol] == "M":
                                continue
                            tmp = int(vis[nrow][ncol]) + 1
                            vis[nrow][ncol] = str(tmp)

    return vis

def dfs(row, col, board, actualBoard, vis, buttons):
    vis[row][col] = 1
    board[row][col] = "B"
    buttons.add(len(board[0]) * row + col)
    for drow in range(-1, 2):
        for dcol in range(-1, 2):
            nrow = row + drow
            ncol = col + dcol
            if nrow >= 0 and nrow < len(board) and ncol >= 0 and ncol < len(board[0]) and not vis[nrow][ncol]:
                if actualBoard[nrow][ncol] == "0":
                    dfs(nrow, ncol, board, actualBoard, vis, buttons)
                else:
                    board[nrow][ncol] = actualBoard[nrow][ncol]
                    buttons.add(len(board[0]) * nrow + ncol)

def checkSpaces(mineCount, board, actualBoard, buttons):
    cnt = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 'E':
                cnt += 1
    if cnt == mineCount:
        for i in range(len(board)):
            for j in range(len(board[0])):
                val = i*len(board[0]) + j
                if actualBoard[i][j] == 'M':
                    buttons[val].config(image=mine_icon, state=tk.DISABLED)
        return True
    return False

def markMinesAtEnd(board, actualBoard, buttons, disabledbuttons):
    for i in range(len(board)):
        for j in range(len(board[0])):
            val = i*len(board[0]) + j
            if actualBoard[i][j] == 'M':
                if val in disabledbuttons:
                    buttons[val].config(image=flag_icon, state=tk.DISABLED)
                    disabledbuttons.remove(val)
                else:
                    buttons[val].config(image=mine_icon, state=tk.DISABLED)
    for i in disabledbuttons:
        buttons[i].config(image=wrong_flag_icon, state=tk.DISABLED)

def playerClicks(crow, ccol, board, actualBoard, vis, mineCount, buttons, buttonsClear, disabledbuttons):
    if actualBoard[crow][ccol] == "M":
        markMinesAtEnd(board, actualBoard, buttons, disabledbuttons)
        return "Lost"
    elif actualBoard[crow][ccol] != "0":
        board[crow][ccol] = actualBoard[crow][ccol]
    else:
        dfs(crow, ccol, board, actualBoard, vis, buttonsClear)
    if checkSpaces(mineCount, board, actualBoard, buttons):
        return "Win"

    return "Cont"

def create_board(board, actualBoard, coordinates, vis, buttonsclear, mineCount, dimensions):
    n = len(board)
    m = len(board[0])
    dimOfRow = dimensions[0][0]
    dimOfCol = dimensions[0][1]
    disabledbuttons = []

    def close():
        print("Closing, Thanks for Playing!")
        root.destroy()
        sys.exit()
    
    def handle_left_click(value, buttons):
        if value == -1:
            root.destroy()
            details = generateRandomBoard(dimOfRow, dimOfCol)
            newboard = details[0]
            newmineCount = details[1]
            create_board(makeGameboard(newboard), numberMineBoard(newboard), makeCoordinates(
                newboard), makeVisited(newboard), buttonsclear, newmineCount, dimensions)
        
        button = buttons[value]
        row = coordinates[value][0]
        col = coordinates[value][1]

        if value not in disabledbuttons:
            if playerClicks(row, col, board, actualBoard, vis, mineCount,  buttons, buttonsclear, disabledbuttons) == "Lost":
                response = messagebox.askyesno(
                    "Game Over", "PLAY AGAIN?", icon='warning')
                if response:
                    root.destroy()
                    details = generateRandomBoard(dimOfRow, dimOfCol)
                    newboard = details[0]
                    newmineCount = details[1]
                    create_board(makeGameboard(newboard), numberMineBoard(newboard), makeCoordinates(
                        newboard), makeVisited(newboard), buttonsclear, newmineCount, dimensions)
                else:
                    close()
            elif playerClicks(row, col, board, actualBoard, vis, mineCount,  buttons, buttonsclear,disabledbuttons) == 'Win':
                buttonlabel = actualBoard[row][col]
                button.config(image=number_icons[buttonlabel], state=tk.DISABLED)
                response = messagebox.askyesno(
                    "You Won!", "PLAY AGAIN?", icon='info')
                if response:
                    root.destroy()
                    details = generateRandomBoard(dimOfRow, dimOfCol)
                    newboard = details[0]
                    newmineCount = details[1]
                    create_board(makeGameboard(newboard), numberMineBoard(newboard), makeCoordinates(
                        newboard), makeVisited(newboard), buttonsclear, newmineCount, dimensions)
                else:
                    close()

            else:
                playerClicks(row, col, board, actualBoard, vis,
                            mineCount,  buttons, buttonsclear,disabledbuttons)
                buttonlabel = actualBoard[row][col]
                button.config(image=number_icons[buttonlabel], state=tk.DISABLED)
                for button_index in buttonsclear:
                    label_text = actualBoard[coordinates[button_index][0]][coordinates[button_index][1]]
                    buttons[button_index].config(image=number_icons[label_text], state=tk.DISABLED)
                buttonsclear.clear()

    def handle_right_click(value, buttons):
        button = buttons[value]
        if value not in disabledbuttons:
            button.config(image=flag_icon)
            disabledbuttons.append(value)
        else:
            button.config(image=tile_icon)
            disabledbuttons.remove(value)
    
    def closeExisting():
        root.destroy()
        backToMainMenu()

    root = tk.Tk()
    root.title("Minesweeper")
    root.resizable(False, False)

    # Load icons
    global flag_icon, mine_icon, tile_icon, wrong_flag_icon, number_icons
    flag_icon = ImageTk.PhotoImage(Image.open("flag.jpg").resize((TILE_SIZE, TILE_SIZE)))
    mine_icon = ImageTk.PhotoImage(Image.open("mine.jpg").resize((TILE_SIZE, TILE_SIZE)))
    tile_icon = ImageTk.PhotoImage(Image.open("tile.jpg").resize((TILE_SIZE, TILE_SIZE)))
    wrong_flag_icon = ImageTk.PhotoImage(Image.open("empty.jpg").resize((TILE_SIZE, TILE_SIZE)))
    
    number_icons = {
        "0": ImageTk.PhotoImage(Image.open("zero.png").resize((TILE_SIZE, TILE_SIZE))),
        "1": ImageTk.PhotoImage(Image.open("one.png").resize((TILE_SIZE, TILE_SIZE))),
        "2": ImageTk.PhotoImage(Image.open("two.png").resize((TILE_SIZE, TILE_SIZE))),
        "3": ImageTk.PhotoImage(Image.open("three.png").resize((TILE_SIZE, TILE_SIZE))),
        "4": ImageTk.PhotoImage(Image.open("four.png").resize((TILE_SIZE, TILE_SIZE))),
        "5": ImageTk.PhotoImage(Image.open("five.png").resize((TILE_SIZE, TILE_SIZE))),
        "6": ImageTk.PhotoImage(Image.open("six.png").resize((TILE_SIZE, TILE_SIZE))),
        "7": ImageTk.PhotoImage(Image.open("seven.png").resize((TILE_SIZE, TILE_SIZE))),
        "8": ImageTk.PhotoImage(Image.open("eight.png").resize((TILE_SIZE, TILE_SIZE))),
    }

    label = tk.Label(root, text="")
    label.grid(row=0, column=0, columnspan=m)
    buttons = []
    for i in range(n):
        for j in range(m):
            value = i * m + j
            button = tk.Button(root, image=tile_icon, width=TILE_SIZE, height=TILE_SIZE, borderwidth=1)
            button.bind("<Button-1>", lambda event, value=value: handle_left_click(value, buttons))
            button.bind("<Button-3>", lambda event, value=value: handle_right_click(value, buttons))
            buttons.append(button)
            button.grid(row=i+1, column=j, padx=0, pady=0)

    button_frame = tk.Frame(root)
    button_frame.grid(row=n+1, column=0, columnspan=m, pady=10)

    new_board_button = tk.Button(button_frame, text="New Board")
    new_board_button.bind("<Button-1>", lambda event, value=value: handle_left_click(-1, buttons))
    new_board_button.pack(side=tk.LEFT, padx=5)

    additional_button = tk.Button(button_frame, text="Main Menu", command=closeExisting)
    additional_button.pack(side=tk.LEFT, padx=5)

    root.protocol("WM_DELETE_WINDOW", close)

    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    root.mainloop()

def makeCoordinates(board):
    coordinates = {}
    for i in range(len(board)):
        for j in range(len(board[0])):
            coordinates[i*len(board[0]) + j] = (i, j)
    return coordinates

def makeVisited(board):
    vis = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
    return vis

def makeGameboard(board):
    gameboard = [['E' for _ in range(len(board[0]))]
                 for _ in range(len(board))]
    return gameboard

def backToMainMenu():
    dimensions = []

    def left_click(value):
        if value == 1:
            dimensions.append([6, 15])
        elif value == 2:
            dimensions.append([10, 25])
        elif value == 3:
            dimensions.append([14, 35])
        root.destroy()

    def on_closing():
        root.destroy()
        sys.exit()

    root = tk.Tk()
    root.title("Minesweeper")

    window_width = 400
    window_height = 200
    root.geometry(f"{window_width}x{window_height}")

    # Center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"+{x}+{y}")

    instruction_label = tk.Label(
        root, text="Choose Difficulty:", font=("Arial", 16, "bold"))
    instruction_label.pack(pady=(30, 10))

    button_frame = tk.Frame(root)
    button_frame.pack(pady=20)

    easy_button = tk.Button(button_frame, text="Easy", padx=20, pady=10, bg="#4CBB17", command=lambda: left_click(1))
    medium_button = tk.Button(button_frame, text="Medium", padx=20, pady=10, bg="#FFC300", command=lambda: left_click(2))
    hard_button = tk.Button(button_frame, text="Hard", padx=20, pady=10, bg="#FF033E", command=lambda: left_click(3))

    easy_button.grid(row=0, column=0, padx=10)
    medium_button.grid(row=0, column=1, padx=10)
    hard_button.grid(row=0, column=2, padx=10)

    root.protocol("WM_DELETE_WINDOW", on_closing)

    root.mainloop()

    details = generateRandomBoard(dimensions[0][0], dimensions[0][1])
    board = details[0]
    mineCount = details[1]

    buttonsclear = set()
    create_board(makeGameboard(board), numberMineBoard(board), makeCoordinates(
        board), makeVisited(board), buttonsclear, mineCount, dimensions)

backToMainMenu()