import threading
import Pyro4

from .models import User
from .rmi_send_file import RmiSendFile
from .tk.tk_chat import TkChat


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RmiClient:
    def __init__(self, ui: TkChat, user: User):
        self.ui = ui
        self.user = user
        self._register()

    def _register(self):
        self.daemon = Pyro4.Daemon()
        self.uri = self.daemon.register(self)

        thread = threading.Thread(target=self.daemon.requestLoop)
        thread.daemon = True
        thread.start()

    def add_message(self, message):
        if self.ui.running:
            self.ui.add_message(message)

    def user_connected(self, username):
        if self.ui.running:
            self.ui.add_user(username)

    def user_disconnected(self, username):
        if self.ui.running:
            self.ui.remove_user(username)

    def user_removed(self):
        if self.ui.running:
            self.ui.handle_close()

    def receive_file(self) -> Pyro4.URI:
        send_file = RmiSendFile(self.daemon)
        uri = str(self.daemon.register(send_file))
        return uri

    @property
    def username(self):
        return self.user.username

    def __eq__(self, other):
        return self.username == other.username

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username
