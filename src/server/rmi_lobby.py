from .rmi_chat import RmiChat
from .models import Room

import Pyro4
import threading


class RmiLobby():
	def __init__(self, hostname='192.168.100.20', port=25501):
		"""hostname : str (default='localhost') - address which the daemon should run.
		- port : int (default=25501) - port which the daemon should run.
		- logs chats and hosts it. use 'register' to create new chats."""
		self.daemon = Pyro4.Daemon(host=hostname, port=port)

	def daemon_loop(self):
		"""Starts the daemon"""
		self.d_thread = threading.Thread(target=self.daemon.requestLoop)
		self.d_thread.daemon = True
		self.d_thread.start()

	def register(self, chat_p) -> str:
		"""Logs a new chat to the daemon and hosts it.
		- chat_p : None - A nameless chat is created and hosted.
		- chat_p : str - creates a chat named as {chat_p} and registers it.
		- chat_p : chat.RmiChat - registers the chat."""
		if isinstance(chat_p, str):
			return self.register(RmiChat(name=chat_p))
		elif chat_p is None:
			return self.register(RmiChat())
		elif isinstance(chat_p, RmiChat):
			return str(self.daemon.register(chat_p))

