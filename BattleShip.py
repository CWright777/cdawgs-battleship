from random import randint
from random import choice


class Ship(object):
    def __init__(self, size):
        self.size = size
        self.status = "alive"
        self.hits = []
        self.location = []

    def update_status(self):
        self.status = "dead"

class Player(object):
    def __init__(self):
        self.sunk = []
        self.ships = []
        self.placed_ships = []
        self.board = []

        def create_fleet():
            small_ships = [Ship(1) for i in range(1)]
            for ship in small_ships:
                self.ships.append(ship)
            medium_ships = [Ship(2) for i in range(1)]
            for ship in medium_ships:
                self.ships.append(ship)
            large_ships = [Ship(3) for i in range(1)]
            for ship in large_ships:
                self.ships.append(ship)
        create_fleet()



def generate_board(player):
    for x in range(7):
        player.board.append(["?"] * 7)


def print_board(board):
    for row in board:
        print " ".join(row)


print "Let's play Battleship!"

# Generate a random row
def random_row(board):
    return randint(0, len(board) - 1)


# Generate a random coloumn
def random_col(board):
    return randint(0, len(board[0]) - 1)


# Show where ships are generated for debugging purposes
def show_ship_locations(player):
    for ship in player.ships:
        player.board[player.ship[0]][player.ship[1]] = "B"
    print_board(player.board)


# Used to find a free space on the board
def find_free_space(player):
    point = [random_row(player.board)] + [random_col(player.board)]
    while True:
        if point in player.placed_ships:
            point = [random_row(player.board)] + [random_col(player.board)]
        else:
            return point


# select direction is used to find a point that is left, right, up or down.
def select_direction(rand, point):
    switcher = {
        0: [point[0], point[1] - 1, 0],  # left
        1: [point[0], point[1] + 1, 1],  # right
        2: [point[0] - 1, point[1], 2],  # up
        3: [point[0] + 1, point[1], 3]  # down
    }
    return switcher.get(rand, False)


# Used to find a point that is adjacent to a given point
def find_adjacent_space(rand_a, rand_b, point, coordinates):
    direction = select_direction(randint(rand_a, rand_b), choice(point))
    while True:
        if direction[0] == -1 or direction[0] == 7 or direction[1] == -1 or direction[1] == 7:
            direction = select_direction(randint(rand_a, rand_b), choice(point))
        elif direction[0:2] in coordinates:
            direction = select_direction(randint(rand_a, rand_b), choice(point))
        else:
            return direction


# generate_ships loops through each ship in the list ships. Then it selects a ranndom point from the board. Saves that
# point and then finds adjacent points as needed by the ship's ship size.
def generate_ships(player):
    for ship in range(0, len(player.ships)):
        point = find_free_space(player)
        player.placed_ships.append(point)
        player.ships[ship].location.append(point)
        if player.ships[ship].size > 1:
            direction = find_adjacent_space(0, 3, [point], player.placed_ships)
            player.placed_ships.append(direction[0:2])
            player.ships[ship].location.append(direction[0:2])
            if player.ships[ship].size > 2:
                if direction[2] == 0 or direction[2] == 1:
                    direction2 = find_adjacent_space(0, 1, [point, direction[0:2]], player.placed_ships)
                    player.placed_ships.append(direction2[0:2])
                    player.ships[ship].location.append(direction2[0:2])
                elif direction[2] == 2 or direction[2] == 3:
                    direction2 = find_adjacent_space(2, 3, [point, direction[0:2]], player.placed_ships)
                    player.placed_ships.append(direction2[0:2])
                    player.ships[ship].location.append(direction2[0:2])


def guess_and_check(player):
    guess_row = int(raw_input("Guess Row:"))
    guess_col = int(raw_input("Guess Col:"))
    guess_total = [guess_row] + [guess_col]
    if (guess_row < 0 or guess_row > 6) or (guess_col < 0 or guess_col > 6):
        print "Oops, that's not even in the ocean."
    elif (player.board[guess_row][guess_col] == "O"):
        print "You guessed that one already."
    for ship in range(0, len(player.ships)):
        if guess_total in player.ships[ship].location:
            player.ships[ship].hits.append(guess_total)
            if player.ships[ship].hits == player.ships[ship].location:
                player.ships[ship].update_status()
                for status in player.ships:
                    if status.status == "dead":
                        player.sunk.append(1)
                    if sum(player.sunk) == len(player.ships):
                        player.board[guess_row][guess_col] = "X"
                        return 0
                    elif player.ships[ship].size == len(player.ships[ship].hits):
                        print "You sunk a Battlship!"
                        player.board[guess_row][guess_col] = "X"
                        break
            else:
                print "Hit!"
                player.board[guess_row][guess_col] = "X"
                break
        elif guess_total not in player.placed_ships:
            print "You missed my battleship!"
            player.board[guess_row][guess_col] = "O"
            break


# play_game is the current version of a very basic form  of battleship
def play_game():
    player_count = int(raw_input("1 or 2 players?:"))
    if player_count == 1:
        player1 = Player()
        generate_board(player1)
        generate_ships(player1)
        for turn in range(49):
            print player1.placed_ships
            print_board(player1.board)
            if guess_and_check(player1) == 0:
                print "You sunk their last Battlship! You Won!"
                break
    elif player_count == 2:
        player1 = Player()
        generate_board(player1)
        generate_ships(player1)
        player2 = Player()
        generate_board(player2)
        generate_ships(player2)
        for turn in range(98):
            if turn % 2 == 1:
                print player1.placed_ships
                if guess_and_check(player1) == 0:
                    print "You sunk their last Battlship! You Won!"
                    break
            if turn % 2 == 0:
                print player2.placed_ships
                if guess_and_check(player2) == 0:
                    print "You sunk their last Battlship! You Won!"
                    break

play_game()