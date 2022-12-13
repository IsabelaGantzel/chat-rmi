import re
from typing import List

from .models import User, Room
from .api import INVALID_PASSWORD, USER_ALREADY_EXISTS, USER_NOT_FOUND, Api
from .chat import Chat

MENU_OPTION_SIGNIN = 1
MENU_OPTION_SIGNUP = 2

MENU_OPTION_JOIN_ROOM = 1
MENU_OPTION_CREATE_ROOM = 2

ROOM_MODE_UNIQUE_ADMIN = 1
ROOM_MODE_ROTATE_ADMIN = 2


def get_value():
    return input("  - ").strip()


# User


def get_username():
    while True:
        value = input("  Usuário (! para abortar): ")

        if value == "!":
            return None

        if re.match(r"[^a-zA-Z0-9]", value):
            print("Erro: Nome do usuário não deve conter caracteres especiais")
            continue

        return value


def get_password():
    while True:
        value = input("  Senha (! para abortar): ")

        if value == "!":
            return None

        if len(value) < 4:
            print("Erro: Senha deve ter no mínimo 4 caracteres")
            continue

        return value


def menu():
    while True:
        print("Menu:")
        print("  1. Entrar")
        print("  2. Cadastrar")

        value = get_value()

        if value == "1":
            return MENU_OPTION_SIGNIN
        if value == "2":
            return MENU_OPTION_SIGNUP

        print(f"Erro: Opção inválida: {value}")


def signin(api: Api):
    print("=" * 50)
    print("Entrar:")

    while True:
        username = get_username()

        if username is None:
            print("Operação abortada")
            print("=" * 50)
            return None

        password = get_password()

        if password is None:
            print("Operação abortada")
            print("=" * 50)
            return None

        (user, error) = api.signin(username, password)

        if error == USER_NOT_FOUND:
            print("Erro: Usuário não encontrado!")
            continue

        if error == INVALID_PASSWORD:
            print("Erro: Senha incorreta!")
            continue

        print("Usuário conectado!")
        print("=" * 50)
        return user


def signup(api: Api):
    print("=" * 50)
    print("Cadastrar:")

    while True:
        username = get_username()

        if username is None:
            print("Operação abortada")
            return None

        password = get_password()

        if password is None:
            print("Operação abortada")
            return None

        (user, error) = api.signup(username, password)

        if error == USER_ALREADY_EXISTS:
            print("Erro: Usuário já cadastrado")
            continue

        print("Usuário cadastrado!")
        print("=" * 50)
        return user


def menu_interactive(api: Api):
    while True:
        option = menu()

        if option == MENU_OPTION_SIGNIN:
            result = signin(api)
            if result is not None:
                return result

        if option == MENU_OPTION_SIGNUP:
            signup(api)


# Rooms


def room_menu(api: Api):
    while True:
        print()
        print("Menu das salas:")
        print("  1. Entrar em uma sala")
        print("  2. Criar uma sala")

        value = get_value()

        if value == "1":
            rooms = api.get_rooms()

            if len(rooms) == 0:
                print("Erro: Não existem salas para entrar")
                continue

            return (rooms, MENU_OPTION_JOIN_ROOM)
        if value == "2":
            return (None, MENU_OPTION_CREATE_ROOM)

        print(f"Erro: Opção inválida: {value}")


def select_room(rooms: List[Room]) -> Room:
    while True:
        print("Chats disponíveis:")
        for n, room in enumerate(rooms):
            print(f"  {n}: {room.name}")

        value = get_value()

        if re.match(r"[^0-9]+", value):
            print("Erro: Informe um número")
            continue

        value = int(value)

        if value >= len(rooms):
            print("Erro: Número inválido")

        return rooms[value]


def get_room_mode():
    return ROOM_MODE_UNIQUE_ADMIN

    while True:
        print("Modos de sala:")
        print("  - 1. Administrador rotativo")
        print("  - 2. Administrador único")

        value = get_value()

        if value == "1":
            return ROOM_MODE_UNIQUE_ADMIN

        if value == "2":
            return ROOM_MODE_ROTATE_ADMIN

        print(f"Erro: Opção inválida: {value}")


def room_interactive(api: Api, logged_user: User):
    while True:
        (rooms, option) = room_menu(api)

        if option == MENU_OPTION_JOIN_ROOM:
            room = select_room(rooms)
            Chat(api, room, logged_user)
            break

        if option == MENU_OPTION_CREATE_ROOM:
            room_mode = get_room_mode()
            room = api.register_room(logged_user.id, room_mode)
            Chat(api, room, logged_user)
            break
