from tkinter import *
from tkinter import ttk
import copy
import time


try:
    xrange
except NameError:
    xrange = range

MARGIN = 20  # Pixels around the board
SIDE = 50  # Width of every board cell.
WIDTH = HEIGHT = MARGIN * 2 + SIDE * 9  # Width and height of the whole board

class Sudoku:

    def __init__(self,s):
        self.S = copy.deepcopy(s)
        self.steps=[]

    def pre(self):
        self.empty = []
        for i in range(9):
            for j in range(9):
                if self.S[i][j] == 0:
                    self.empty.append((i,j))
#         self.empty.reverse()


    def find(self,i1,j1,k):
        for i in range(9):
            if i != i1:
                if self.S[i][j1] == k:
                    return 0
            if i !=  j1:
                if self.S[i1][i] == k:
                    return 0
        i_l = (i1//3)*3
        j_l = (j1//3)*3
        for i in range(i_l,i_l+3):
            for j in range(j_l,j_l+3):
                if i!=i1 and j!=j1:
                    if self.S[i][j] == k:
                        return 0
        return 1

    def print_(self):
        for i in range(9):
            print(self.S[i])


    def fit(self):
        self.pre()
        #print(self.empty())
        self.solve()
        #return self.steps

    def solve(self):
        if len(self.empty) == 0:
            return True
        (i,j) = self.empty[-1]

        if i == None:
            return True
        else:
            self.empty.remove((i,j))

        for k in range(1,10):
            if self.find(i,j,k) == 1:
                self.S[i][j] = k
                self.steps.append([i,j,k])
                if self.solve():
                    break
                else:
                    self.S[i][j] = 0

        if self.S[i][j] == 0 :
            self.empty.append((i,j))
            return False

        return True



def restart(frame,show=False):
    for widget in frame.winfo_children():
        widget.destroy()
    g = Sudoku_Board(frame, s)
    if show:
        g.Sol_Steps()




class Sudoku_Board(Frame):

    def __init__(self, parent, game):
        self.game = copy.deepcopy(game)
        self.game_result = Sudoku(game)
        self.game_result.fit()
        self.steps_of_algo = copy.deepcopy(self.game_result.steps)
        self.parent = parent
        Frame.__init__(self, parent)

        self.row, self.col = 0, 0

        self.__initUI()

    def __initUI(self):
        #self.parent.text("Sudoku")
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self,width=WIDTH,height=HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        clear_button = Button(self,text="Clear answers",command=self.__clear_answers)
        clear_button.pack(fill=BOTH, side=BOTTOM)

        self.__draw_grid()
        self.__draw_puzzle()

        self.canvas.bind("<Button-1>", self.__cell_clicked)
        self.canvas.bind("<Key>", self.__key_pressed)
        self.canvas.bind("<space>",self.print_)

    def print_(self,e):
        restart(self.parent,True)

    def __draw_grid(self):
        """
        Draws grid divided with blue lines into 3x3 squares
        """
        for i in xrange(10):
            color = "blue" if i % 3 == 0 else "gray"

            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color)

    def __draw_puzzle(self):
        self.canvas.delete("numbers")
        for i in xrange(9):
            for j in xrange(9):
                answer = self.game[i][j]
                if answer != 0:
                    x = MARGIN + j * SIDE + SIDE / 2
                    y = MARGIN + i * SIDE + SIDE / 2
                    original = s[i][j]
                    color = "black" if answer == original else "sea green"
                    if(answer != original):
                        if not self.check_valid(i,j):
                            color = "red"
                    self.canvas.create_text(
                        x, y, text=answer, tags="numbers", fill=color
                    )
    def __cell_clicked(self, event):
        if self.check_win():
            return
        x, y = event.x, event.y
        if (MARGIN < x < WIDTH - MARGIN and MARGIN < y < HEIGHT - MARGIN):
            self.canvas.focus_set()

            # get row and col numbers from x,y coordinates
            row, col = (y - MARGIN) // SIDE, (x - MARGIN) // SIDE

            # if cell was selected already - deselect it
            if (row, col) == (self.row, self.col):
                self.row, self.col = -1, -1
            elif s[row][col] == 0:
                self.row, self.col = row, col

        self.__draw_cursor()

    def __key_pressed(self, event):
        if self.check_win():
            return
        if self.row >= 0 and self.col >= 0 and event.char in "1234567890":
            if s[self.row][self.col] ==0:
                self.game[self.row][self.col] = int(event.char)
            self.col, self.row = -1, -1
            self.__draw_puzzle()
            self.__draw_cursor()
            if self.check_win():
                self.__draw_victory()

    def __draw_cursor(self):
        self.canvas.delete("cursor")
        if self.row >= 0 and self.col >= 0:
            x0 = MARGIN + self.col * SIDE + 1
            y0 = MARGIN + self.row * SIDE + 1
            x1 = MARGIN + (self.col + 1) * SIDE - 1
            y1 = MARGIN + (self.row + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )

    def __show_cursor(self,i,j):
        self.canvas.delete("cursor")
        if i >= 0 and j >= 0:
            x0 = MARGIN + j * SIDE + 1
            y0 = MARGIN + i * SIDE + 1
            x1 = MARGIN + (j + 1) * SIDE - 1
            y1 = MARGIN + (i + 1) * SIDE - 1
            self.canvas.create_rectangle(
                x0, y0, x1, y1,
                outline="red", tags="cursor"
            )


    def __clear_answers(self):
        restart(self.parent,False)


    def __draw_victory(self):
        # create a oval (which will be a circle)
        x0 = y0 = MARGIN + SIDE * 2
        x1 = y1 = MARGIN + SIDE * 7
        self.canvas.create_oval(
            x0, y0, x1, y1,
            tags="victory", fill="dark orange", outline="orange"
        )
        # create text
        x = y = MARGIN + 4 * SIDE + SIDE / 2
        self.canvas.create_text(
            x, y,
            text="You win!", tags="winner",
            fill="white", font=("Arial", 32)
        )

    def check_win(self):
        for i in xrange(9):
            for j in xrange(9):
                if self.game[i][j] != self.game_result.S[i][j]:
                    return False
        return True

    def check_valid(self,row,col):
        k = self.game[row][col]
        for i in range(9):
            if i != row:
                if self.game[i][col] == k:
                    return 0
            if i !=  col:
                if self.game[row][i] == k:
                    return 0
        i_l = (row//3)*3
        j_l = (col//3)*3
        for i in range(i_l,i_l+3):
            for j in range(j_l,j_l+3):
                if i!=row and j!=col:
                    if self.game[i][j] == k:
                        return 0
        return 1

    def Sol_Steps(self):
        if len(self.steps_of_algo) != 0:
            item = self.steps_of_algo[0]
            #print(len(self.steps_of_algo))
            self.game[item[0]][item[1]] = item[2]
            self.__draw_puzzle()
            self.__show_cursor(item[0],item[1])
            self.steps_of_algo.pop(0)
            self.canvas.after(100,self.Sol_Steps)




s = [[7, 8, 0, 4, 0, 0, 1, 2, 0],
    [6, 0, 0, 0, 7, 5, 0, 0, 9],
    [0, 0, 0, 6, 0, 1, 0, 7, 8],
    [0, 0, 7, 0, 4, 0, 2, 6, 0],
    [0, 0, 1, 0, 5, 0, 9, 3, 0],
    [9, 0, 4, 0, 6, 0, 0, 0, 5],
    [0, 7, 0, 3, 0, 0, 0, 1, 2],
    [1, 2, 0, 0, 0, 7, 4, 0, 0],
    [0, 4, 9, 2, 0, 6, 0, 0, 7]]

root = Tk()
mainnotebook = ttk.Notebook(root)
mainnotebook.grid(row=0, column=0, columnspan=3)
board = Frame(mainnotebook)
board.grid(row=0, column=0, columnspan=3)
mainnotebook.add(board, text="Table")
mainwindow=Sudoku_Board(board,s)

root.mainloop()
