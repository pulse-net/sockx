"""
Client that sends the file (uploads)
"""
import socket
import tqdm
import os

from ..constants import *


class UDPFileSender:
    def __init__(self, receiver_ip, port=PORT):
        self.__receiver_ip = receiver_ip
        self.__port = port

    def send_file(self, filename):
        # Get the file size
        filesize = os.path.getsize(filename)

        # Create the client UDP socket
        s = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        # Address to send to
        addr = (self.__receiver_ip, self.__port)

        # Send the filename and filesize
        s.sendto(f"{filename}{SEPARATOR}{filesize}".encode(), addr)

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
                s.sendto(bytes_read, addr)

                # Update the progress bar
                progress.update(len(bytes_read))

        s.sendto(bytes(END_DATA, encoding="utf-8"), addr)
