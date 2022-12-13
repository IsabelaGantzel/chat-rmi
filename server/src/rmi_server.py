from typing import NamedTuple
import Pyro4

Client = NamedTuple("Client", [("proxy", Pyro4.Proxy), ("username", str), ("uri", str)])


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RmiServer:
    def __init__(self, name: str):
        self._name = name
        self._messages = []
        self.uri = None
        self.clients = {}

    def connect(self, uri):
        proxy = Pyro4.Proxy(uri)
        client = Client(proxy, proxy.username, uri)
        self.clients[uri] = client
        self._broadcast_message(f"User '{client.username}' has joined the chat", uri)
        self._broadcast_connected(uri)

    def disconnect(self, uri):
        client = self.clients[uri]
        self._broadcast_message(f"User '{client.username}' has disconnected.", uri)
        self._broadcast_disconnected(uri)
        del self.clients[uri]

    def send_message(self, message, uri):
        if uri not in self.clients:
            return

        self._broadcast_message(message, uri)

    def send_private_message(self, message, other_username, uri):
        if uri not in self.clients:
            return

        print("[INFO]", message)
        for other_client in self.clients.values():
            if other_client.username == other_username:
                other_client.proxy.add_message(message)
                return

    def get_connected_users(self):
        return [client.username for client in self.clients.values()]

    def delete_user(self, username):
        for client in self.clients.values():
            if client.username == username:
                client.proxy.user_removed()
                return

    def get_messages(self):
        return self._messages

    def get_name(self):
        return self._name

    def _broadcast_disconnected(self, uri):
        client = self.clients[uri]
        for other_client in self.clients.values():
            if other_client.uri == client.uri:
                continue
            other_client.proxy.user_disconnected(client.username)

    def _broadcast_connected(self, uri):
        client = self.clients[uri]
        for other_client in self.clients.values():
            if other_client.uri == client.uri:
                continue
            other_client.proxy.user_connected(client.username)

    def _broadcast_message(self, message, uri=None):
        print("[INFO]", message)
        self._messages.append(message)
        for other_client in self.clients.values():
            if other_client.uri == uri:
                continue
            other_client.proxy.add_message(message)

    def __str__(self):
        return f"chat named {self._name}"
