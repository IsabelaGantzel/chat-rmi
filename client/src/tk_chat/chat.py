import queue
import threading
import time

from ..api import Api
from ..models import Room, User
from ..rmi_client import RmiClient
from ..rmi_send_file import RmiSendFile
from ..rmi_server import RmiServer
from ..tk.tk_alert import tk_alert
from ..tk.tk_chat import TkChat
from ..tk.tk_file import tk_file

ACTION_DELETE = 1
ACTION_SEND_FILE = 2


def chat(api: Api, room: Room, user: User):
    actions = queue.Queue()

    def actions_task():
        while True:
            (action, data) = actions.get()

            if action == ACTION_DELETE:
                other_user = data

                if other_user is None:
                    continue

                if rmi_server is None:
                    time.sleep(0.1)
                    actions.put(other_user)
                    continue

                rmi_server.delete_user(other_user)

            if action == ACTION_SEND_FILE:
                other_user = data

                filepath = tk_file.askopenfilename(title="Informe o caminho do arquivo")

                if len(filepath) == 0:
                    continue

                send_file_uri = rmi_server.send_file(other_user)
                if send_file_uri is None:
                    tk_alert.showerror(
                        "Erro",
                        "Falha ao se conectar com o outro cliente",
                    )
                    continue

                rmi_send_file = RmiSendFile.create(send_file_uri)
                rmi_send_file.open_file(filepath)

                completed = False
                BUFFER_SIZE = 4096
                with open(filepath, "rb") as file:
                    while True:
                        data = file.read(BUFFER_SIZE)
                        if len(data) == 0:
                            completed = True
                            break

                        if not rmi_send_file.send_data(data):
                            break

                if completed:
                    rmi_send_file.complete()
                    tk_alert.showinfo(
                        "Arquivo enviado",
                        "Arquivo enviado com sucesso!",
                    )
                else:
                    tk_alert.showerror(
                        "Erro",
                        "Falha ao enviar dados para o outro cliente",
                    )

    thread = threading.Thread(target=actions_task)
    thread.daemon = True
    thread.start()

    def on_send_message(other_user, message):
        if other_user is None:
            message = f"{user.username}: {message}"
            rmi_client.add_message(message)
            rmi_server.send_message(message, rmi_client.uri)
        else:
            message = f"{user.username} -> {other_user}: {message}"
            rmi_client.add_message(message)
            rmi_server.send_private_message(message, other_user, rmi_client.uri)

    def on_send_file(other_user):
        actions.put((ACTION_SEND_FILE, other_user))

    def on_delete(other_user):
        actions.put((ACTION_DELETE, other_user))

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
        ui = TkChat(admin)

        rmi_client = RmiClient(ui, user)
        rmi_server = RmiServer.create(room.uri)

        rmi_server.connect(rmi_client.uri)
        ui.set_title(
            f"{rmi_server.get_name()} ({'*admin' if admin else user.username})"
        )

        api.connect_to_room(user.id, room.id)

        for username in rmi_server.get_connected_users():
            if username != user.username:
                ui.add_user(username)

        for message in rmi_server.get_messages():
            ui.add_message(message)

        ui.on_send_file = on_send_file
        ui.on_send_message = on_send_message
        ui.on_close = on_close
        ui.on_delete = on_delete
        ui.run()
    except Exception as e:
        on_close()
        raise e
