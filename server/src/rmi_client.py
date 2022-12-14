import Pyro4

class RmiClient:
    @staticmethod
    def create(uri: str) -> "RmiClient":
        rmi_client = Pyro4.Proxy(uri)
        return rmi_client

    def add_message(self, message):
        ...

    def user_connected(self, username):
        ...

    def user_disconnected(self, username):
        ...

    def user_removed(self):
        ...

    def receive_file(self) -> Pyro4.URI:
        ...

    @property
    def username(self) -> str:
        ...
