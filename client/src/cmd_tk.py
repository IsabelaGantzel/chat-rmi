import Pyro4

from .api import Api, USER_ALREADY_EXISTS, USER_NOT_FOUND, INVALID_PASSWORD
from .tk.signin import TkSignin
from .tk.signup import TkSignup
from .tk.chat import TkChat
from .tk.alert import alert
from .models import User, Room
from .rmi_client import RmiClient
from src.cmd import (
    menu,
    room_menu,
    select_room,
    get_room_mode,
    MENU_OPTION_SIGNIN,
    MENU_OPTION_SIGNUP,
    MENU_OPTION_JOIN_ROOM,
    MENU_OPTION_CREATE_ROOM,
)


def signin(api: Api):
    def on_submit(username, password):
        result = api.signin(username, password)
        error = result[1]

        if error is None:
            nonlocal user
            user = result[0]
            return ui.destroy()

        if error == USER_NOT_FOUND:
            return alert.showerror("Erro", "Usuário não encontrado!")

        if error == INVALID_PASSWORD:
            return alert.showerror("Erro", "Senha incorreta!")

    user = None
    ui = TkSignin()
    ui.on_submit = on_submit
    ui.run()
    return user


def signup(api: Api):
    def on_submit(username, password):
        (_, error) = api.signup(username, password)

        if error is None:
            return ui.destroy()

        if error == USER_ALREADY_EXISTS:
            return alert.showerror("Erro", "Usuário já cadastrado")

    ui = TkSignup()
    ui.on_submit = on_submit
    ui.run()


def menu_interactive(api: Api):
    while True:
        option = menu()

        if option == MENU_OPTION_SIGNIN:
            result = signin(api)
            if result is not None:
                return result

        if option == MENU_OPTION_SIGNUP:
            signup(api)


def chat(api: Api, room: Room, user: User):
    def on_send_message(other_user, message):
        if other_user is None:
            message = f"{user.username}: {message}"
            rmi_client.incoming_message(message)
            rmi_server.send_message(message, rmi_client.uri)

    def on_send_file(other_user):
        print(other_user)

    def on_close():
        if rmi_client is not None and rmi_server is not None:
            rmi_server.disconnect(rmi_client.uri)
        api.disconnect_to_room(user.id, room.id)

    rmi_client = None
    rmi_server = None
    try:
        ui = TkChat(user.username)

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
        ui.run()
    except Exception as e:
        on_close()
        raise e


def room_interactive(api: Api, logged_user: User):
    while True:
        (rooms, option) = room_menu(api)

        if option == MENU_OPTION_JOIN_ROOM:
            room = select_room(rooms)
            chat(api, room, logged_user)
            return

        if option == MENU_OPTION_CREATE_ROOM:
            room_mode = get_room_mode()
            room = api.register_room(logged_user.id, room_mode)
            chat(api, room, logged_user)
            return
