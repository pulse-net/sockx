"""
Client that sends the file (uploads)
"""
import socket
import tqdm
import os

from ..constants import *
from ..utils.error import ConnectionFailure


class TCPFileSender:
    def __init__(self, receiver_ip, port=PORT):
        self.__receiver_ip = receiver_ip
        self.__port = port

    def send_file(self, filename):
        # Get the file size
        filesize = os.path.getsize(filename)

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

        # Send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # Start sending the file
        progress = tqdm.tqdm(
            range(filesize),
            f"Sending {filename}",
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
        )
        with open(filename, "rb") as f:
            while True:
                # Read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # File transmitting is done
                    break

                # We use sendall to assure transimission in busy networks
                s.sendall(bytes_read)

                # Update the progress bar
                progress.update(len(bytes_read))

        # Close the socket
        s.close()
