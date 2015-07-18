from random import randint

board = []

numberOfShips = 3
currentShips = []
sunkShips = 0
for x in range(5):
    board.append(["O"] * 5)

def print_board(board):
    for row in board:
        print " ".join(row)

print "Let's play Battleship!"
print_board(board)

def random_row(board):
    return randint(0, len(board) - 1)

def random_col(board):
    return randint(0, len(board[0]) - 1)

def generateShips():
    for ship in range(0, numberOfShips):
        ship = [str(random_row(board)) + ", " + str(random_col(board))]
        while ship in currentShips:
            ship = str(random_row(board)) + ", " + str(random_col(board))
        else:
            currentShips.append(ship)
    return currentShips

#    if random_row(board) != ship_row and random_col(board) != ship_col:
#        ship2_row = random_col(board)

# Everything from here on should go in your for loop!
# Be sure to indent four spaces!
generateShips()
print currentShips
for turn in range(4):
    print "Turn", turn + 1
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Col:"))
    guessTotal = [str(guess_row) + ", " + str(guess_col)]
    if guessTotal in currentShips:
        sunkShips += 1
        if sunkShips == numberOfShips:
            print"You won"
            break
        else:
            print "Congratulations! You sunk a battleship!"
    else:
        if (guess_row < 0 or guess_row > 4) or (guess_col < 0 or guess_col > 4):
            print "Oops, that's not even in the ocean."
        elif(board[guess_row][guess_col] == "X"):
            print "You guessed that one already."
        else:
            print "You missed my battleship!"
            board[guess_row][guess_col] = "X"
    if turn == 3:
        print "Game Over"
    # Print (turn + 1) here!
print_board(board)
