from .rmi_lobby import RmiLobby

import src.server.auth as auth
import src.server.db as db

import json
import threading
import socket as sk

class Server():
	def __init__(self, hostname='192.168.100.20', port=25500, lobby_port=25501):
		"""This class works as a DNS server for the chats.
		- hostname : str (default='localhost') - address which the server should run.
		- port : int (default=25500) - port which the server should run.
		- lobby_port : int (default=25501) - port which the daemon should run."""

		print("Setting up daemon")
		self.lobby = RmiLobby(hostname=hostname, port=lobby_port)
		self.lobby.daemon_loop()

		print("Setting up server")
		self._server = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
		self._server.bind((hostname, port))

	def run(self):
		self.s_thread = threading.Thread(target=self._run)
		self.s_thread.daemon=True
		self.s_thread.start()

	def _run(self):
		print("Running server")
		self._server.listen()

		while True:
			conn, _ = self._server.accept()
			message = conn.recv(2048).decode('utf-8')

			if message.startswith("POST signin;"):
				values = message.split(';')
				result = auth.signin(values[1], values[2])
				conn.send(json.dumps(result).encode())

			if message.startswith("POST signup;"):
				values = message.split(';')
				result = auth.signup(values[1], values[2])
				conn.send(json.dumps(result).encode())

			if message == 'GET rooms':
				result = db.get_rooms()
				conn.send(json.dumps(result).encode())

			if message.startswith("POST register-room;"):
				values = message.split(';')
				user_id = values[1]

				rooms_count = db.get_next_room_id()
				room_name = f"Sala {rooms_count}"

				uri = self.lobby.register(room_name)
				user = db.get_user_by_id(user_id) 

				result = None
				if user is not None:
					chat_mode = values[2]
					result = db.register_room(user.id, room_name, uri, chat_mode)

				conn.send(json.dumps(result).encode())

			if message.startswith("POST connect-to-room;"):
				values = message.split(';')
				result = db.register_user_in_room(values[1], values[2])
				conn.send(json.dumps(result).encode())

			if message.startswith("POST disconnect-to-room;"):
				values = message.split(';')
				user_id = values[1]
				room_id = values[2]
				users = db.get_room_users(room_id)

				if len(users) == 1:
					db.remove_room(room_id)
				elif len(users) > 1:
					room = db.get_room_by_id(room_id)

					if room.owner_id == user_id:
						db.remove_room(room_id)
					else:
						db.remove_user_in_room(user_id, room_id)

				conn.send(json.dumps(None).encode())

			conn.close()
