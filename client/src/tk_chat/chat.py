import queue
import threading
import time
import Pyro4

from ..api import Api
from ..models import Room, User
from ..rmi_client import RmiClient
from ..tk.tk_chat import TkChat


def chat(api: Api, room: Room, user: User):
    messages = queue.Queue()

    def delete_task():
        while True:
            other_user = messages.get()

            if other_user is None:
                continue

            if rmi_server is None:
                time.sleep(0.1)
                messages.put(other_user)
                continue

            rmi_server.delete_user(other_user)

    thread = threading.Thread(target=delete_task)
    thread.daemon = True
    thread.start()

    def on_send_message(other_user, message):
        if other_user is None:
            message = f"{user.username}: {message}"
            rmi_client.add_message(message)
            rmi_server.send_message(message, rmi_client.uri)

    def on_send_file(other_user):
        print(other_user)

    def on_delete(other_user):
        messages.put(other_user)

    def on_close():
        try:
            if rmi_client is not None and rmi_server is not None:
                rmi_server.disconnect(rmi_client.uri)
                api.disconnect_to_room(user.id, room.id)
        except Exception:
            pass

    rmi_client = None
    rmi_server = None
    try:
        admin = user.id == room.owner_id
        ui = TkChat(user.username, admin)

        rmi_client = RmiClient(ui, user)
        rmi_server = Pyro4.Proxy(room.uri)

        rmi_server.connect(rmi_client.uri)

        api.connect_to_room(user.id, room.id)

        for username in rmi_server.get_connected_users():
            if username != user.username:
                ui.add_user(username)

        for message in rmi_server.get_last_messages():
            ui.add_message(message)

        ui.on_send_file = on_send_file
        ui.on_send_message = on_send_message
        ui.on_close = on_close
        ui.on_delete = on_delete
        ui.run()
    except Exception as e:
        on_close()
        raise e
