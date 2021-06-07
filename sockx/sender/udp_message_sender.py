"""
Client that sends the message
"""
import socket

from ..constants import *


class UDPMessageSender:
    def __init__(self, host, port=PORT):
        self.__host = host
        self.__port = port

    def send_message(self, message):
        # Create the client UDP socket
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Address to send to
        addr = (self.__host, self.__port)

        # Send the filename and filesize
        s.sendto(message.encode(), addr)
