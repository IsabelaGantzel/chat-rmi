from .rmi_server import RmiServer

import Pyro4
import threading


class RmiLobby:
    def __init__(self, hostname, port):
        """hostname : str (default='localhost') - address which the daemon should run.
        - port : int (default=25501) - port which the daemon should run.
        - logs chats and hosts it. use 'register' to create new chats."""
        self.daemon = Pyro4.Daemon(host=hostname, port=port)

    def run(self):
        """Starts the daemon"""
        self.d_thread = threading.Thread(target=self.daemon.requestLoop)
        self.d_thread.daemon = True
        self.d_thread.start()

    def register(self, name: str) -> RmiServer:
        server = RmiServer(name)
        server.uri = str(self.daemon.register(server))
        return server

    def unregister(self, chat_p):
        """Unregisters a chat from the daemon.
        - chat_p : str - unregisters the chat with the uri {chat_p}.
        - chat_p : chat.RmiChat - unregisters the chat."""
        if isinstance(chat_p, str):
            self.daemon.unregister(chat_p)
        elif isinstance(chat_p, RmiServer):
            self.daemon.unregister(chat_p)
