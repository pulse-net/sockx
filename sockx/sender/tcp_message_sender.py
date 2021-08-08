"""
Client that sends the message
"""
import socket

from ..constants import *
from ..utils.error import ConnectionFailure


class TCPMessageSender:
    def __init__(self, receiver_ip, port=PORT):
        self.__receiver_ip = receiver_ip
        self.__port = port

    def send_message(self, message):
        # Create the client TCP socket
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)

        print(f"[+] Connecting to {self.__receiver_ip}:{self.__port}")
        s.settimeout(MAX_TIMEOUT)

        try:
            s.connect((self.__receiver_ip, self.__port))
        except socket.timeout:
            raise ConnectionFailure("Connection timed out, make sure the receiver is in same network!")
        except ConnectionRefusedError:
            raise ConnectionFailure("Connection refused by receiver, make sure you have pressed receive in receiver!")

        s.settimeout(None)
        print("[+] Connected.")

        # Send the message
        s.send(message.encode())

        # Close the socket
        s.close()
