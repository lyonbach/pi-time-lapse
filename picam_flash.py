import socket
import constants
import time

def _send_command(command):

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((constants.HOST, constants.PORT))
    client_socket.sendall(command)
    client_socket.close()


def turn_on():

    _send_command(constants.TURN_ON)

def turn_off():

    _send_command(constants.TURN_OFF)

def stop_server():

    _send_command(constants.STOP)

