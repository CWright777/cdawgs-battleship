__author__ = 'CDawg'
import socket
import thread
import struct
from random import randint
from random import choice


class Ship(object):
    def __init__(self):
        self.hits = []
        self.location = []
        self.status = "alive"

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
        return switcher.get(choice(direction))

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
                    if direction[0] <= -1 or direction[0] >= self.size or direction[1] <= -1 or \
                            direction[1] == self.size:
                        del unused_directions[direction[3]]
                        direction = self.select_direction(choice(unused_directions), choice(point))
                    elif direction[0:2] in self.placed_ships or direction[0:2] in point:
                        direction = self.select_direction(choice(unused_directions), choice(point))
                    else:
                        return direction
                except IndexError:
                    return Exception


class Player(object):
    def __init__(self, name):
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
                        direction = self.board.find_adjacent_space(ship.location, "any")
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

    @staticmethod
    def guess_and_check(guess_total, player):
        if (guess_total[0] < 0 or guess_total[0] > 6) or (guess_total[1] < 0 or guess_total[1] > 6):
            return "Oops, that's not even in the ocean."
        elif player.board.board[guess_total[0]][guess_total[1]] == "O":
            return "You guessed that one already."
        for ship in player.ships:
            if guess_total in ship.location and guess_total not in ship.hits:
                if guess_total not in ship.hits:
                    ship.hits.append(guess_total)
                    print ship.hits
                if ship.hits == ship.location:
                    player.sunk.append(1)
                    if sum(player.sunk) == len(player.ships):
                        player.board.board[guess_total[0]][guess_total[1]] = "X"
                        return "You sunk their last BattleShip!"
                    elif ship.size == len(ship.hits):
                        player.board.board[guess_total[0]][guess_total[1]] = "X"
                        return "You sunk a Battlship!"
                else:
                    player.board.board[guess_total[0]][guess_total[1]] = "X"
                    return "Hit!"
            elif guess_total not in player.board.placed_ships:
                player.board.board[guess_total[0]][guess_total[1]] = "O"
                return "You missed my battleship!"
        return "You guessed and hit that one already"


class Game(object):
    def __init__(self):
        self.player_name = []
        self.players = []

    @staticmethod
    def generate_assets(player):
            player.board.generate_board()
            player.build(0, SmallShip)
            player.build(0, MediumShip)
            player.build(1, LargeShip)
            player.generate_ships()

    header_struct = struct.Struct('!I')

    @staticmethod
    def recvall(sock, length):
        blocks = []
        while length != 0:
            block = sock.recv(length)
            if not block:
                raise EOFError('socket closed with %d bytes left'
                               ' in this block'.format(length))
            length -= len(block)
            blocks.append(block)
        return b''.join(blocks)

    def get_block(self, sock):
        data = self.recvall(sock, self.header_struct.size)
        (block_length,) = self.header_struct.unpack(data)
        return self.recvall(sock, block_length)

    def put_block(self, sock, message):
        block_length = len(message)
        sock.send(self.header_struct.pack(block_length))
        sock.send(message)

    def get_data(self, conn):
        while True:
            block = self.get_block(conn)
            if not block:
                break
            try:
                return list(struct.unpack('!5s2I', block))
            except Exception:
                return block

    def get_player_count(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 6668))
        sock.listen(5)
        print('Listening at', sock.getsockname())
        print('Waiting for a connection')

        def client_thread(conn):
                data = self.get_data(conn)
                print data[0:2]
                if data[0] == "count":
                    print self.players[0].board.placed_ships
                    conn.close()
                elif data[0] == "guess":
                    guess_total = data[1:3]
                    self.put_block(conn, self.players[0].guess_and_check(guess_total, self.players[0]))
                    self.put_block(conn, b'')
                    print guess_total
                    conn.close()
                else:
                    print data
                    print self.player_name
                    if data not in self.player_name:
                        new_player = Player(data)
                        self.players.append(new_player)
                        self.generate_assets(new_player)
                        self.put_block(conn, "good")
                        self.put_block(conn, b'')
                    else:
                        self.put_block(conn, "nope")
                        self.put_block(conn, b'')
                conn.close()

        while True:
            conn, addr = sock.accept()
            thread.start_new_thread(client_thread, (conn,))

    def start(self):
        for turn in range(50):
            self.get_player_count()

game1 = Game()
game1.start()
