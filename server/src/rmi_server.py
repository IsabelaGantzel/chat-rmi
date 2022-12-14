from typing import NamedTuple
import Pyro4

from .rmi_client import RmiClient

Client = NamedTuple("Client", [("proxy", RmiClient), ("username", str), ("uri", str)])


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RmiServer:
    def __init__(self, name: str):
        self.name = name
        self.messages = []
        self.uri = None
        self.clients = {}

    def close(self):
        for client in self.clients.values():
            client.proxy.user_removed()

    def connect(self, uri):
        proxy = RmiClient.create(uri)
        client = Client(proxy, proxy.username, uri)
        self.clients[uri] = client
        self._broadcast_connected(uri)

    def disconnect(self, uri):
        self._broadcast_disconnected(uri)
        del self.clients[uri]

    def send_message(self, message, uri):
        self._broadcast_message(message, uri)

    def send_private_message(self, message, other_username, _uri):
        print("[INFO]", message)
        client = self._get_client_by_username(other_username)
        if client is not None:
            client.proxy.add_message(message)

    def get_connected_users(self):
        return [client.username for client in self.clients.values()]

    def delete_user(self, username):
        client = self._get_client_by_username(username)
        if client is not None:
            client.proxy.user_removed()

    def get_messages(self):
        return self.messages

    def get_name(self):
        return self.name

    def send_file(self, username: str) -> None:
        client = self._get_client_by_username(username)
        if client is not None:
            return client.proxy.receive_file()

    def _get_client_by_username(self, username: str):
        for client in self.clients.values():
            if client.username == username:
                return client

    def _broadcast_disconnected(self, uri: Pyro4.URI):
        client = self.clients[uri]
        for other_client in self.clients.values():
            if other_client.uri == client.uri:
                continue
            other_client.proxy.user_disconnected(client.username)

    def _broadcast_connected(self, uri: Pyro4.URI):
        client = self.clients[uri]
        for other_client in self.clients.values():
            if other_client.uri == client.uri:
                continue
            other_client.proxy.user_connected(client.username)

    def _broadcast_message(self, message, uri=None):
        print("[INFO]", message)
        self.messages.append(message)
        for other_client in self.clients.values():
            if other_client.uri == uri:
                continue
            other_client.proxy.add_message(message)

    def __str__(self):
        return f"chat named {self.name}"
