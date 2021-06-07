from ..constants import *
from ..utils import error
from .tcp_file_sender import TCPFileSender
from .tcp_message_sender import TCPMessageSender
from .udp_file_sender import UDPFileSender
from .udp_message_sender import UDPMessageSender


class Sender:
    @staticmethod
    def get_sender(host, port=PORT, protocol=PROTOCOL, is_message=False):
        if protocol == "TCP":
            if not is_message:
                return TCPFileSender(host=host, port=port)

            return TCPMessageSender(host=host, port=port)
        elif protocol == "UDP":
            if not is_message:
                return UDPFileSender(host=host, port=port)

            return UDPMessageSender(host=host, port=port)
        else:
            raise error.InvalidSocketProtocol(
                message=f"Protocol {protocol} not known, cannot create sender instance!"
            )
