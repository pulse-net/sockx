from ..constants import *
from ..utils import error
from .tcp_file_sender import TCPFileSender
from .tcp_message_sender import TCPMessageSender
from .udp_file_sender import UDPFileSender
from .udp_message_sender import UDPMessageSender


class Sender:
    @staticmethod
    def get_sender(receiver_ip, port=PORT, protocol=PROTOCOL, is_message=False):
        if protocol == "TCP":
            if not is_message:
                return TCPFileSender(receiver_ip=receiver_ip, port=port)

            return TCPMessageSender(receiver_ip=receiver_ip, port=port)
        elif protocol == "UDP":
            if not is_message:
                return UDPFileSender(receiver_ip=receiver_ip, port=port)

            return UDPMessageSender(receiver_ip=receiver_ip, port=port)
        else:
            raise error.InvalidSocketProtocol(
                message=f"Protocol {protocol} not known, cannot create sender instance!"
            )
