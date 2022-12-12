import json 
import socket
from typing import Tuple

from .models import User, Room

Server = Tuple[str, int]

def send_request(server: Server, message: str):
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	socket.connect(server)
	socket.send(message.encode())
	serialized = socket.recv(4096).decode('utf-8')
	return json.loads(serialized)


class Api:
    def __init__(self, server: str, port: int) -> None:
        self.server = server
        self.port = port
        self.socket = None
    
    def _initilize(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server, self.port))
    
    def _send(self, message):
        self.socket.send(message.encode())
        serialized = self.socket.recv(4096).decode('utf-8')
        return json.loads(serialized)

    def _request(self, message: str):
        self._initilize()
        return self._send(message)

    def signin(self, username: str, password: str):
        result = self._request(f"POST signin;{username};{password}")
        result[0] = User(*result[0]) if result[0] is not None else None
        return result

    def signup(self, username: str, password: str):
        result = self._request(f"POST signup;{username};{password}")
        result[0] = User(*result[0]) if result[0] is not None else None
        return result

    def get_rooms(self):
        result = self._request("GET rooms")
        return [Room(*it) for it in result]

    def register_room(self, user_id: int, room_mode: int):
        result = self._request(f"POST register-room;{user_id};{room_mode}")
        return Room(*result) if result is not None else None

    def connect_to_room(self, user_id: int, room_id: int) -> str:
        return self._request(f"POST connect-to-room;{user_id};{room_id}")
    
    def disconnect_to_room(self, user_id: int, room_id: int) -> None:
        self._request(f"POST disconnect-to-room;{user_id};{room_id}")
