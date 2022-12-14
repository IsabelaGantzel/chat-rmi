from .rmi_server import RmiServer

import Pyro4
import threading


class RmiLobby:
    def __init__(self, hostname, port):
        """hostname : str (default='localhost') - address which the daemon should run.
        - port : int (default=25501) - port which the daemon should run.
        - logs chats and hosts it. use 'register' to create new chats."""
        self.daemon = Pyro4.Daemon(host=hostname, port=port)
        self.servers = {}

    def run(self) -> None:
        """Starts the daemon"""
        self.d_thread = threading.Thread(target=self.daemon.requestLoop)
        self.d_thread.daemon = True
        self.d_thread.start()

    def register(self, name: str) -> RmiServer:
        server = RmiServer(name)
        server.uri = str(self.daemon.register(server))
        self.servers[server.uri] = server
        return server

    def unregister(self, uri: str) -> None:
        # server = self.servers[uri]
        # server.close()
        self.daemon.unregister(uri)
        del self.servers[uri]
