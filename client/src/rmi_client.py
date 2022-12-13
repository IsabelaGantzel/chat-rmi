import threading
import Pyro4
from .models import User
from .tk.tk_chat import TkChat


@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RmiClient:
    def __init__(self, ui: TkChat, user: User):
        self.ui = ui
        self.user = user
        self._register()

    def _register(self):
        daemon = Pyro4.Daemon()
        self.uri = daemon.register(self)

        thread = threading.Thread(target=daemon.requestLoop)
        thread.daemon = True
        thread.start()

    def incoming_message(self, message):
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

    @property
    def username(self):
        return self.user.username

    def __eq__(self, other):
        return self.username == other.username

    def __str__(self):
        return self.username

    def __repr__(self):
        return self.username
