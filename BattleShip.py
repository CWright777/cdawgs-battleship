from random import randint
from random import choice

class Ship(object):
    def __init__(self):
        self.hits = []
        self.location = []
        self.status  = "alive"

    def update_status(self):
        self.status = "dead"

class SmallShip(Ship):
    size = 1

class MediumShip(Ship):
    size = 2

class LargeShip(Ship):
    size = 3

class Board(object):
    def __init__(self, size):
        self.placed_ships = []
        self.board = []
        self.size = size

    def generate_board(self):
        for col in range(self.size):
            self.board.append(["?"] * self.size)

    def print_board(self):
        for row in self.board:
            print " ".join(row)

    # Generate a random row
    def random_row(self):
        return randint(0, len(self.board) - 1)

    # Generate a random column
    def random_col(self):
        return randint(0, len(self.board[0]) - 1)

    # Used to find a free space on the board
    def find_free_space(self):
        point = [self.random_row()] + [self.random_col()]
        while True:
            if point in self.placed_ships:
                point = [self.random_row()] + [self.random_col()]
            else:
                return point

    # select direction is used to find a point that is left, right, up or down.
    @staticmethod
    def select_direction(direction, point):
        switcher = {
            "left": [point[0], point[1] - 1, 0],  # left
            "right": [point[0], point[1] + 1, 1],  # right
            "up": [point[0] - 1, point[1], 2],  # up
            "down": [point[0] + 1, point[1], 3]  # down
        }
        return switcher.get(choice(direction), False)

    # Used to find a point that is adjacent to a given point
    def find_adjacent_space(self, point, hor_ver):
        unused_directions = ["left", "right", "up", "down"]
        if hor_ver == "hor":
            del unused_directions[2:4]
        elif hor_ver == "ver":
            del unused_directions[0:2]
        while True:
            direction = self.select_direction(unused_directions, choice(point))
            while True:
                try:
                    if direction[0] <= -1 or direction[0] >= self.size or direction[1] <= -1 or direction[1] == self.size:
                        del unused_directions[direction[3]]
                        direction = self.select_direction(choice(unused_directions), choice(point))
                    elif direction[0:2] in self.placed_ships or direction[0:2] in point:
                        direction = self.select_direction(choice(unused_directions), choice(point))
                    else:
                        return direction
                except IndexError:
                    return Exception


class Player(object):
    def __init__(self,name):
        self.sunk = []
        self.ships = []
        self.board = Board(7)
        self.name = name

    def build(self, quantity, model):
        fleet = [model() for i in range(quantity)]
        for ship in fleet:
            self.ships.append(ship)

    # generate_ships loops through each ship in the list ships. Then it selects a ranndom point from the board. Saves that
    # point and then finds adjacent points as needed by the ship's ship size.
    def generate_ships(self):
        for ship in self.ships:
            while True:
                try:
                    point = self.board.find_free_space()
                    ship.location.append(point)
                    if ship.size > 1:
                        direction = self.board.find_adjacent_space(ship.location,"any")
                        ship.location.append(direction[0:2])
                        if ship.size > 2:
                            for next_point in range(ship.size - 2):
                                if direction[2] == 0 or direction[2] == 1:
                                    next_point = self.board.find_adjacent_space(ship.location, "hor")
                                    ship.location.append(next_point[0:2])
                                elif direction[2] == 2 or direction[2] == 3:
                                    next_point = self.board.find_adjacent_space(ship.location, "ver")
                                    ship.location.append(next_point[0:2])
                    break
                except Exception:
                    ship.location = []
            for coordinate in ship.location:
                self.board.placed_ships.append(coordinate)

    # Show where ships are generated for debugging purposes
    def show_ship_locations(self):
        for point in self.board.placed_ships:
            self.board.board[point[0]][point[1]] = "B"
        self.board.print_board()

    @staticmethod
    def input_guess(prompt):
        while True:
            guess = raw_input(prompt)
            try:
                if guess < 0 or guess > 6:
                    return int(guess)
            except ValueError:
                print "Try again, that didn't seem like a usable number!"

    def guess_and_check(self):
        guess_row = self.input_guess("Guess Row:")
        guess_col = self.input_guess("Guess Col:")
        guess_total = [guess_row] + [guess_col]
        if (guess_row < 0 or guess_row > 6) or (guess_col < 0 or guess_col > 6):
            return "Oops, that's not even in the ocean."
        elif self.board.board[guess_row][guess_col] == "O":
            return "You guessed that one already."
        for ship in self.ships:
            if guess_total in ship.location and guess_total not in ship.hits:
                if guess_total not in ship.hits:
                    ship.hits.append(guess_total)
                if ship.hits == ship.location:
                    self.sunk.append(1)
                    if sum(self.sunk) == len(self.ships):
                        self.board.board[guess_row][guess_col] = "X"
                        return 0
                    elif ship.size == len(ship.hits):
                        self.board.board[guess_row][guess_col] = "X"
                        return "You sunk a Battlship!"
                else:
                    self.board.board[guess_row][guess_col] = "X"
                    return "Hit!"
            elif guess_total not in self.board.placed_ships:
                self.board.board[guess_row][guess_col] = "O"
                return "You missed my battleship!"
        return "You guessed and hit that one already"

class Game(object):
    def __init__(self):
        self.players = []

    def determine_player_count(self):
        while True:
            player_count = Player.input_guess("1 or 2 players?:")
            if player_count > 0 or player_count < 3:
                player = [Player("Player " + str(i + 1)) for i in range(player_count)]
                for i in player:
                    self.players.append(i)
                break

    def generate_assets(self):
        for player in self.players:
            player.board.generate_board()
            player.build(0,SmallShip)
            player.build(0,MediumShip)
            player.build(12,LargeShip)
            player.generate_ships()

    def play_game(self):
        for turn in range(50):
            x = turn % len(self.players)
            print self.players[x].name
            self.players[x].board.print_board()
            print self.players[x].board.placed_ships
            outcome = self.players[x].guess_and_check()
            if outcome == 0:
                print "You sunk their last Battlship! " + self.players[x].name + " Wins!"
                break
            else:
                print outcome

    def start(self):
        self.determine_player_count()
        self.generate_assets()
        self.play_game()




print "Let's play Battleship!"

game1 = Game()
game1.start()
