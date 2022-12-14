import Pyro4


class RmiServer:
    @staticmethod
    def create(uri: str) -> "RmiServer":
        rmi_server = Pyro4.Proxy(uri)
        return rmi_server

    def connect(self, uri: str) -> None:
        ...

    def disconnect(self, uri: str) -> None:
        ...

    def send_message(self, message: str, uri: str) -> None:
        ...

    def send_private_message(self, message: str, other_username: str, uri: str) -> None:
        ...

    def get_connected_users(self) -> list[str]:
        ...

    def delete_user(self, username: str) -> None:
        ...

    def get_messages(self) -> list[str]:
        ...

    def get_name(self) -> str:
        ...

    def send_binary_data(self, data: bin) -> None:
        ...
