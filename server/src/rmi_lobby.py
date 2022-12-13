from .rmi_server import RmiServer

import Pyro4
import threading


class RmiLobby:
    def __init__(self, hostname, port):
        """hostname : str (default='localhost') - address which the daemon should run.
        - port : int (default=25501) - port which the daemon should run.
        - logs chats and hosts it. use 'register' to create new chats."""
        self.daemon = Pyro4.Daemon(host=hostname, port=port)

    def daemon_loop(self):
        """Starts the daemon"""
        self.d_thread = threading.Thread(target=self.daemon.requestLoop)
        self.d_thread.daemon = True
        self.d_thread.start()

    def register(self, chat_p) -> str:
        """Logs a new chat to the daemon and hosts it.
        - chat_p : None - A nameless chat is created and hosted.
        - chat_p : str - creates a chat named as {chat_p} and registers it.
        - chat_p : chat.RmiChat - registers the chat."""
        if isinstance(chat_p, str):
            return self.register(RmiServer(name=chat_p))
        elif chat_p is None:
            return self.register(RmiServer())
        elif isinstance(chat_p, RmiServer):
            return str(self.daemon.register(chat_p))

    def unregister(self, chat_p):
        """Unregisters a chat from the daemon.
        - chat_p : str - unregisters the chat with the uri {chat_p}.
        - chat_p : chat.RmiChat - unregisters the chat."""
        if isinstance(chat_p, str):
            self.daemon.unregister(chat_p)
        elif isinstance(chat_p, RmiServer):
            self.daemon.unregister(chat_p)
