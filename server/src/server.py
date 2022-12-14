from .rmi_lobby import RmiLobby

import src.auth as auth
import src.db as db

import json
import threading
import socket as sk


class Server:
    def __init__(self, hostname, port, lobby_port):
        """This class works as a DNS server for the chats.
        - hostname : str (default='localhost') - address which the server should run.
        - port : int (default=25500) - port which the server should run.
        - lobby_port : int (default=25501) - port which the daemon should run."""

        print("Setting up daemon")
        self.lobby = RmiLobby(hostname=hostname, port=lobby_port)
        self.lobby.run()

        print("Setting up server")
        self._server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
        self._server.bind((hostname, port))

    def run(self):
        self.s_thread = threading.Thread(target=self._run)
        self.s_thread.daemon = True
        self.s_thread.start()

    def _run(self):
        print("Running server")
        self._server.listen()

        db.clean_rooms()
        while True:
            conn, _ = self._server.accept()
            message = conn.recv(2048).decode("utf-8")

            if message.startswith("POST signin;"):
                values = message.split(";")
                result = auth.signin(values[1], values[2])
                conn.send(json.dumps(result).encode())

            if message.startswith("POST signup;"):
                values = message.split(";")
                result = auth.signup(values[1], values[2])
                conn.send(json.dumps(result).encode())

            if message == "GET rooms":
                result = db.get_rooms()
                conn.send(json.dumps(result).encode())

            if message.startswith("POST register-room;"):
                values = message.split(";")
                user_id = values[1]
                user = db.get_user_by_id(user_id)

                rooms_count = db.get_next_room_id()
                room_name = f"Sala {rooms_count} - {user.username}"

                server_rmi = self.lobby.register(room_name)

                result = None
                if user is not None:
                    chat_mode = values[2]

                    rooms = db.get_rooms_by_owner(user_id)
                    for room in rooms:
                        db.remove_room(room.id)
                        self.lobby.unregister(room.id)

                    result = db.register_room(
                        user.id, room_name, server_rmi.uri, chat_mode
                    )

                conn.send(json.dumps(result).encode())

            if message.startswith("POST connect-to-room;"):
                values = message.split(";")
                result = db.register_user_in_room(values[1], values[2])
                conn.send(json.dumps(result).encode())

            if message.startswith("POST disconnect-to-room;"):
                values = message.split(";")
                use_case = DisconectUserUseCase(self.lobby)
                use_case.execute(user_id=values[1], room_id=values[2])
                conn.send(json.dumps(None).encode())

            conn.close()


class DisconectUserUseCase:
    def __init__(self, lobby: RmiLobby) -> None:
        self.lobby = lobby

    def execute(self, user_id: int, room_id: int):
        room = db.get_room_by_id(room_id)

        if room is None:
            return

        user = db.get_user_by_id(user_id)

        if user is None:
            return

        users_in_room = db.get_room_users(room_id)

        if len(users_in_room) <= 1:
            db.remove_room(room.id)
            self.lobby.unregister(room.uri)
            return

        if False and room.owner_id == user.id:
            db.remove_room(room.id)
            self.lobby.unregister(room.uri)
        else:
            db.remove_user_in_room(user.id, room.id)
