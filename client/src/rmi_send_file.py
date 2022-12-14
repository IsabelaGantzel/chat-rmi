import Pyro4
import base64
from pathlib import Path


@Pyro4.expose
class RmiSendFile:
    def __init__(self, daemon: Pyro4.Daemon) -> None:
        self.filename = None
        self.file = None
        self.daemon = daemon
        self.completed = False

    def open_file(self, filename: str):
        dirpath = Path.home() / "Downloads"
        dirpath.mkdir(exist_ok=True)
        self.filename = dirpath / Path(filename).name
        self.file = self.filename.open(mode="wb")

    def send_data(self, data: dict):
        if self.completed and self.file is None:
            return False

        try:
            base64str = base64.b64decode(data["data"])
            self.file.write(base64str)
            return True
        except:
            return False

    def complete(self):
        self.completed = True
        self.file.close()
        self.daemon.unregister(self)

    @staticmethod
    def create(uri: str) -> "RmiSendFile":
        rmi_send_file = Pyro4.Proxy(uri)
        return rmi_send_file
