__author__ = 'CDawg'
import socket
import struct


def input_guess(prompt):
    while True:
        guess = raw_input(prompt)
        try:
            if guess < 0 or guess > 6:
                return int(guess)
        except ValueError:
            print "Try again, that didn't seem like a usable number!"


def get_player_count():
    while True:
        player_count = input_guess("1 or 2 players?:")
        if player_count > 0 or player_count < 3:
            return player_count

header_struct = struct.Struct('!I')


def get_block(sock):
    data = recvall(sock, header_struct.size)
    (block_length,) = header_struct.unpack(data)
    return recvall(sock, block_length)


def put_block(sock, message):
    block_length = len(message)
    sock.send(header_struct.pack(block_length))
    sock.send(message)


def recvall(sock, length):
    blocks = []
    while length:
        block = sock.recv(length)
        if not block:
            raise EOFError('socket closed with %d bytes left'
                           ' in this block'.format(length))
        length -= len(block)
        blocks.append(block)
    return b''.join(blocks)


def what_name():
    name = raw_input("What's your username?")
    return name


def client():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 6668))
    put_block(sock,  what_name())
    put_block(sock, b'')
    while True:
        while True:
            block = get_block(sock)
            if not block:
                break
            message = block
        if message == "nope":
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('localhost', 6668))
            put_block(sock, what_name())
            put_block(sock, b'')
        else:
            break
    sock.close()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 6668))
    put_block(sock, struct.pack('!5s2I', "count", get_player_count(), 0))
    put_block(sock, b'')
    sock.close()
    for turn in range(50):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 6668))
        put_block(sock, struct.pack('!5s2I', "guess", input_guess("Guess Row:"), input_guess("Guess Col:")))
        put_block(sock, b'')
        while True:
            block = get_block(sock)
            if not block:
                break
            message = block
        if message == "You sunk their last BattleShip!":
            print'Message:' + message
            sock.close()
            break
        else:
            print'Message:' + message
            sock.close()

client()
