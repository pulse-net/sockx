"""
Client that sends the message
"""
import socket

from ..constants import *


class UDPMessageSender:
    def __init__(self, receiver_ip, port=PORT):
        self.__receiver_ip = receiver_ip
        self.__port = port

    def send_message(self, message):
        # Create the client UDP socket
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Address to send to
        addr = (self.__receiver_ip, self.__port)

        # Send the filename and filesize
        s.sendto(message.encode(), addr)
