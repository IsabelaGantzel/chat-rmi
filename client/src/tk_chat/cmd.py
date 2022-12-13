from ..api import Api
from ..models import User
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

from .signin import signin
from .signup import signup
from .chat import chat


def menu_interactive(api: Api):
    while True:
        option = menu()

        if option == MENU_OPTION_SIGNIN:
            result = signin(api)
            if result is not None:
                return result

        if option == MENU_OPTION_SIGNUP:
            signup(api)


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
