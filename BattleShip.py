from random import randint
from random import choice


class Ship(object):
    def __init__(self, size):
        self.size = size
        self.status = 'alive'
        self.hits = []
        self.location = []


ship1 = Ship(3)
ship2 = Ship(3)
ship3 = Ship(1)
ship4 = Ship(2)
ship5 = Ship(2)

ships = [ship1, ship2, ship3, ship4, ship5]
board = []
current_ships = []

for x in range(7):
    board.append(["?"] * 7)


def print_board(board):
    for row in board:
        print " ".join(row)


print "Let's play Battleship!"

#Generate a random row
def random_row(board):
    return randint(0, len(board) - 1)

#Generate a random coloumn
def random_col(board):
    return randint(0, len(board[0]) - 1)

#Show where ships are generated for debugging purposes
def show_ship_locations():
    for ship in current_ships:
        board[ship[0]][ship[1]] = "B"
    print_board(board)

#Used to find a free space on the board
def find_free_space(coordinates):
    point = [random_row(board)] + [random_col(board)]
    while True:
        if point in coordinates:
            point = [random_row(board)] + [random_col(board)]
        else:
            return point
            break

#select direction is used to find a point that is left, right, up or down.
def select_direction(rand, point):
    switcher = {
        0: [point[0], point[1] - 1, 0],  # left
        1: [point[0], point[1] + 1, 1],  # right
        2: [point[0] - 1, point[1], 2],  # up
        3: [point[0] + 1, point[1], 3]  # down"
    }
    return switcher.get(rand, False)

#Used to find a point that is adjacent to a given point
def find_adjacent_space(rand_a, rand_b, point, coordinates):
    direction = select_direction(randint(rand_a, rand_b), choice(point))
    while True:
        if direction[0] == -1 or direction[0] == 7 or direction[1] == -1 or direction[1] == 7:
            direction = select_direction(randint(rand_a, rand_b), choice(point))
        elif direction[0:2] in coordinates:
            direction = select_direction(randint(rand_a, rand_b), choice(point))
        else:
            return direction
            break

#generate_ships loops through each ship in the list ships. Then it selects a ranndom point from the board. Saves that
#point and then finds adjacent points as needed by the ship's ship size.
def generate_ships():
    for ship in range(0, len(ships)):
        point = find_free_space(current_ships)
        current_ships.append(point)
        ships[ship].location.append(point)
        if ships[ship].size > 1:
            direction = find_adjacent_space(0, 3, [point], current_ships)
            current_ships.append(direction[0:2])
            ships[ship].location.append(direction[0:2])
            if ships[ship].size > 2:
                if direction[2] == 0 or direction[2] == 1:
                    direction2 = find_adjacent_space(0, 1, [point, direction[0:2]], current_ships)
                    current_ships.append(direction2[0:2])
                    ships[ship].location.append(direction2[0:2])
                elif direction[2] == 2 or direction[2] == 3:
                    direction2 = find_adjacent_space(2, 3, [point, direction[0:2]], current_ships)
                    current_ships.append(direction2[0:2])
                    ships[ship].location.append(direction2[0:2])


generate_ships()

#play_game is the current version of a very basic form  of battleship
def play_game():
    print current_ships
    sunk_ships = 0
    for turn in range(4):
        print_board(board)
        print "Turn", turn + 1
        guess_row = int(raw_input("Guess Row:"))
        guess_col = int(raw_input("Guess Col:"))
        guess_total = [guess_row] + [guess_col]
        for ship in ships:
            if guess_total in ship.location:
                ship.hits.append(guess_total)
                if ship.hits == ship.location:
                    sunk_ships += 1
                    if sunk_ships == len(ships):
                        print "You Won"
                        board[guess_row][guess_col] = "X"
                        break
                    else:
                        print "Congratulations! You sunk a battleship!"
                        board[guess_row][guess_col] = "X"
                        break
                else:
                    print "Hit!"
                    board[guess_row][guess_col] = "X"
                    break
            else:
                if (guess_row < 0 or guess_row > 6) or (guess_col < 0 or guess_col > 6):
                    print "Oops, that's not even in the ocean."
                    break
                elif (board[guess_row][guess_col] == "O"):
                    print "You guessed that one already."
                    break
                else:
                    print "You missed my battleship!"
                    board[guess_row][guess_col] = "O"
                    break


play_game()
