from copy import deepcopy


class Board:

    #Board initialization
    #The user can choose the first player and the difficulty level (2 levels)
    #The variable "max" will be used in the miniMax algorithm. It will define whether we "maximize" or "minimize the score.
    #The variable "passed" defines if the current player passed and "winner" if one of the players won.
    def __init__(self, first_player =0, dif = 1):

        self.player = first_player
        self.difficulty = dif
        self.max = first_player
        self.passed = False
        self.winner = False

        #Initializing the board the first state (center boxes) and blank boxes
        self.array = []
        for i in range(8):
            self.array.append([])
            for y in range(8):
                self.array[i].append(" ")

        self.array[3][3] = "O"
        self.array[3][4] = "X"
        self.array[4][3] = "X"
        self.array[4][4] = "O"

        self.previousBoard = self.array


    def printBoard(self):

        print("  1|2|3|4|5|6|7|8")
        for i in range(8):
            string_array = [str(i + 1)]

            for j in range(8):
                if j == 7:
                    if self.previousBoard[i][j] == "O":
                        string_array.append("|O|")
                    elif self.previousBoard[i][j] == "X":
                        string_array.append("|X|")
                    elif self.previousBoard[i][j] == " ":
                        string_array.append("| |")
                else:
                    if self.previousBoard[i][j] == "O":
                        string_array.append("|O")
                    elif self.previousBoard[i][j] == "X":
                        string_array.append("|X")
                    elif self.previousBoard[i][j] == " ":
                        string_array.append("| ")

            print_in_one_line(string_array)

    #Board Update
    #If it's AI's turn, we can choose Alpha Beta pruning or simple MiniMax for the move decision.
    #We check the level of difficulty the user has chosen, in order to decide which heuristic will be used.

    def updateBoard(self):

        if not self.winner:
            if self.player == 1:
                self.previousBoard = self.array
                if self.difficulty == 1:
                    alphaBetaResult = self.alphaBeta(self.array, depth, -float("inf"), float("inf"), 1, 1)
                else:
                    alphaBetaResult = self.alphaBeta(self.array, depth, -float("inf"), float("inf"), 1, 2)

                # Rearrange the board
                self.array = alphaBetaResult[1]

                if len(alphaBetaResult) == 3:
                    position = alphaBetaResult[2]
                    self.previousBoard[position[0]][position[1]] = "X"

                # minimax_result = self.minimax(self.array, depth, self.max)
                # self.array = minimax_result[1]

                self.previousBoard = self.array
                self.player = 1 - self.player
                self.must_pass()
            self.printBoard()

        else:
            print("GAME OVER!")

    #x and y are the coordinates of the user's move
    #We rearrange the board and switch players
    def boardMove(self, x, y):


        self.previousBoard = self.array
        self.previousBoard[x][y] = "O"
        self.array = move(self.array, x, y)
        self.previousBoard = self.array
        self.printBoard()
        self.player = 1 - self.player
        self.must_pass()
        if self.passed: print("pass")
        else: print("Dont need to pass, updating..")
        self.updateBoard()


    #Checks if the current player doesn't have any valid moves to make.
    #If there is at least 1 valid move, it returns false.
    #If there aren't any, it switches players and checks whether or not the other player has passed too.
    #If both of them passed, it means there are not any valid moves for any of them and the game is over.
    #If the other player hasn't pass, we just change the variable "passed" to TRUE.
    def must_pass(self):
        pass_bool = True

        for i in range(8):
            for j in range(8):
                if valid_test(self.array, self.player, i, j):
                    pass_bool = False

        if pass_bool:
            self.player = 1 - self.player
            if self.passed:
                self.winner = True

            else:

                self.passed = True
            self.updateBoard()
        else:
            self.passed = False

    #MiniMax Algorithm
    #The function's input is the board's array(node), the depth the user has chosen(depth), wether or not the AI was the first player(maximize)
    #and which heuristic will be used.
    #The matrix "children" is used as the possible valid moves.
    #The matrix "coordinates" stores the coordinates of every valid move.
    #The function returns the player's score of the best possible move and the board state after that move is made.
    def minimax(self, node, depth, maximize, heuristic):
        children = []
        coordinates = []

        for i in range(8):
            for j in range(8):
                if valid_test(self.array, self.player, i, j):
                    children.append(move(node, i, j))
                    coordinates.append([i, j])

        if depth == 0 or len(coordinates) == 0:
            if heuristic == 1:
                return [score_dumb(self.array, self.player), node]
            else:
                return [score_smart(self.array, self.player), node]
        #If AI was the first player, we must maximize the score
        if maximize:
            bestValue = -float("inf")
            bestBoard = []
            for board in children:
                val = self.minimax(board, depth - 1, self.player)[0]
                if val > bestValue:
                    bestValue = val
                    bestBoard = board
            # print("best score = " + str(bestValue))
            return [bestValue, bestBoard]
        #If AI was the second player, we must minimize the score
        else:
            bestValue = float("inf")
            bestBoard = []
            for board in children:
                val = self.minimax(board, depth - 1, self.player)[0]
                if val < bestValue:
                    bestValue = val
                    bestBoard = board

            # print("best score = " + str(bestValue))
            return [bestValue, bestBoard]

    #Alpha Beta pruning algorithm
    #The function's input is the board's array(node), the depth the user has chosen, alpha, beta, wether or not the AI was the first player(maximize)
    #and which heuristic will be used(dif).
    # The matrix "boards" is used as the possible valid moves.
    # The matrix "choices" stores the coordinates of every valid move.
    # The function returns the player's score of the best possible move, the board state after that move is made and the move's coordinates.
    def alphaBeta(self, node, depth, alpha, beta, maximizing, dif):

            boards = []
            choices = []

            for x in range(8):
                for y in range(8):
                    if valid_test(self.array, self.player, x, y):
                        test = move(node, x, y)
                        boards.append(test)
                        choices.append([x, y])

            if depth == 0 or len(choices) == 0:
                if dif == 1:
                    return [score_dumb(node, maximizing), node]
                else:
                    return [score_smart(node, maximizing), node]

            if maximizing:
                v = -float("inf")
                bestBoard = []
                bestChoice = []
                for board in boards:
                    if dif == 1:
                        boardValue = self.alphaBeta(board, depth - 1, alpha, beta, 0, 1)[0]
                    else:
                        boardValue = self.alphaBeta(board, depth - 1, alpha, beta, 0, 2)[0]

                    if boardValue > v:
                        v = boardValue
                        bestBoard = board
                        bestChoice = choices[boards.index(board)]
                    alpha = max(alpha, v)
                    if beta <= alpha:
                        break
                return [v, bestBoard, bestChoice]
            else:
                v = float("inf")
                bestBoard = []
                bestChoice = []
                for board in boards:
                    if dif == 1:
                        boardValue = self.alphaBeta(board, depth - 1, alpha, beta, 1, 1)[0]
                    else:
                        boardValue = self.alphaBeta(board, depth - 1, alpha, beta, 1, 2)[0]
                    if boardValue < v:
                        v = boardValue
                        bestBoard = board
                        bestChoice = choices[boards.index(board)]
                    beta = min(beta, v)
                    if beta <= alpha:
                        break
                return [v, bestBoard, bestChoice]

#Used for when we need to print many string variables in one line
def print_in_one_line(string_array):
    output = ""
    for i in string_array:
        output += i

    print(output)


def move(given_array, row, column):
    array = deepcopy(given_array)
    if board.player == 0:
        node = "O"
    elif board.player == 1:
        node = "X"
    array[row][column] = node  # we assume the move is valid, we will check it before we call move

    #Find all the nodes near the new node (the one the player chose to move to)
    neighbour_nodes = []

    for i in range(max(0, row - 1), min(8, row + 2)):
        for j in range(max(0, column - 1), min(column + 2, 8)):
            if array[i][j] != " ":
                neighbour_nodes.append([i, j])
    #In "convert" we will store every node that needs to be converted
    convert = []

    #Find all lines
    for n in neighbour_nodes:
        neighbour_row = n[0]
        neighbour_column = n[1]

        line = []

        distance_x = neighbour_row - row
        distance_y = neighbour_column - column

        i = neighbour_row
        j = neighbour_column

        while 0 <= i < 8 and 0 <= j < 8:
            line.append([i, j])
            # If we reach an empty box, break
            if array[i][j] == " ":
                break
            # end of the line of boxes to be converted
            if array[i][j] == node:
                for k in line:
                    convert.append(k)
                break

            i += distance_x
            j += distance_y
    #Convert the nodes
    for c in convert:
        array[c[0]][c[1]] = node

    return array

#Move validation
#We check if the move a player has chosen is valid
def valid_test(given_array, player, row, column):
    if player == 0: node = "O"
    else: node = "X"

    # INVALID MOVES
    #Invalid coordinates
    if row>7 or column>7 or row<0 or column<0:
        print("out of bounds")
        return False
    #There node is not empty
    if given_array[row][column] != " ":

        return False

    else:

        neighbour_nodes = []

        for i in range(max(0, row - 1), min(7, row + 2)):
            for j in range(max(0, column - 1), min(column + 2, 8)):
                if given_array[i][j] != " ":
                    neighbour_nodes.append([i, j])

        if len(neighbour_nodes) == 0:

            return False
        # Search for possible lines
        else:

            v = False

            for n in neighbour_nodes:
                neighbour_row = n[0]
                neighbour_column = n[1]

                if given_array[neighbour_row][neighbour_column] == node:

                    continue  # not valid neighbour
                else:
                    distance_x = neighbour_row - row
                    distance_y = neighbour_column - column

                    i = neighbour_row
                    j = neighbour_column

                    while 0 <= i < 8 and 0 <= j < 8:

                        # If we reach an empty box, break
                        if given_array[i][j] == " ":
                            break
                        # If we find the player's colour, a line is formed and it is a valid move
                        if given_array[i][j] == node:
                            v = True
                            break

                        i += distance_x
                        j += distance_y
        return v

#First heuristic.
#For every node that contains the player's piece we increase the player's score by 1.
#For every node that contains the opponent's piece we decrease the player's score by 1.
def score_dumb(given_array, player):
    s = 0

    if player == 0:
        node = "O"
    else:
        node = "X"

    for x in range(8):
        for y in range(8):

            if given_array[x][y] == node:
                s += 1
            elif given_array[x][y] != " ":
                s -= 1
    return s

#Second heuristic.
#There are position of higher and lower risk.
#The corners worth 5, the nodes at the edges worth 3, the nodes near the corners are worth -3(high risk) and all other nodes worth 1.
#Again for every node that contains the player's piece we increase the player's score by the node's worth
#and for every node that contains the opponent's piece we decrease the player's score by the node's worth.
def score_smart(given_array, player):
    s = 0

    if player == 0:
        node = "O"
    else:
        node = "X"

    for x in range(8):
        for y in range(8):
            # Normal tiles worth 1
            add = 1


            if (x == 0 and y == 1) or (x == 1 and 0 <= y <= 1):
                if given_array[0][0] == node:
                    add = 5
                else:
                    add = -5

            elif (x == 0 and y == 6) or (x == 1 and 6 <= y <= 7):
                if given_array[7][0] == node:
                    add = 5
                else:
                    add = -5

            elif (x == 7 and y == 1) or (x == 6 and 0 <= y <= 1):
                if given_array[0][7] == node:
                    add = 5
                else:
                    add = -5

            elif (x == 7 and y == 6) or (x == 6 and 6 <= y <= 7):
                if given_array[7][7] == node:
                    add = 5
                else:
                    add = -5

            # Edge tiles worth 5
            if (x == 0 and 1 < y < 6) or (x == 7 and 1 < y < 6) or (y == 0 and 1 < x < 6) or (y == 7 and 1 < x < 6):
                add = 5
            # Corner tiles worth 25
            elif (x == 0 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 0) or (x == 7 and y == 7):
                add = 25

            if given_array[x][y] == node:
                s += add
            elif given_array[x][y] != " ":
                s -= add
    return s

#Count how many X's and O's there currently are.
def total(array):
    amount_x = 0
    amount_o = 0
    for x in range(8):
        for y in range(8):
            if array[x][y] == "X":
                amount_x += 1
            if array[x][y] == "O":
                amount_o += 1
    return [amount_x, amount_o]

#Prompt
while True:
    try:
        depth = int(input("Enter depth: (up to 4)"))
        break
    except ValueError:
        print("Oops! That was not valid. Try again...")

while True:
    try:
        difficulty = int(input("Press 1 for dumb, 2 for smart opponent!"))
        break
    except ValueError:
        print("Oops! That was not valid. Try again...")

player_1 = input("Would you like to play first? (Y or N): ")

#Run game
start = Board()
start.printBoard()
if player_1 == "Y" or player_1 == "y":
    print("You play first - O")
    board = Board(0)
elif player_1 == "N" or player_1 == "n":
    print("I play first - X")
    board = Board(1)

while True:

    if board.winner:
        print("GAME OVER!")
        board.player = 1-board.player
        if difficulty == 1:
            print("Winner: " + str(board.player) + " with score: "+str(score_dumb(board.array, board.player)))
        else:
            print("Winner: " + str(board.player) + " with score: " + str(score_smart(board.array, board.player)))
        break

    if board.player == 1:
        print("My turn")
        board.updateBoard()

    else:
        print("Your turn")
        board.must_pass()
        if board.passed:

            board.printBoard()
            continue
        row_pos = int(input("Choose a row: "))
        column_pos = int(input("Choose a column: "))
        v_result = valid_test(board.array, board.player, row_pos-1, column_pos-1)

        if v_result:
            board.boardMove(row_pos-1, column_pos-1)

        else: print("not valid position")

    count_score = total(board.array)
    print("X: " + str(count_score[0]))
    print("O: " + str(count_score[1]))

    #print("Score of " + board.player + ": " + str(score(board.array, board.player)))

