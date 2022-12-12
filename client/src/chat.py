import Pyro4
import tkinter
import threading

from .api import Api
from .models import User, Room

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Chat():
	def create_messages_box(self):
		messages_frame = tkinter.Frame(self.top)
		scrollbar = tkinter.Scrollbar(messages_frame)
		messages = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
		scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
		messages.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
		messages.pack()
		messages_frame.pack()

		self.messages = messages

	def create_window(self):
		self.top = tkinter.Tk()
		self.top.title(self.room.name)

	def create_ui(self):
		self.create_window()
		self.create_messages_box()

	def __init__(self, api: Api, room: Room, user: User):
		"""The instantiation of this class requires:
			- uri : str - uri to connect to chat.
			- username : str - how it shall be displayed for the participants in the chat."""
		print(user)
		print(room)

		self.api = api
		self.user = user
		self.room = room 
		self.chat = Pyro4.Proxy(room.uri)

		self.create_ui()

		#Creating input text field
		self.my_msg = tkinter.StringVar()
		# my_msg.set("Type your messages here.")
		entry_field = tkinter.Entry(self.top, textvariable=self.my_msg)
		entry_field.bind("<Return>", self.send_message)
		entry_field.pack()

		send_button = tkinter.Button(self.top, text="Send", command=self.send_message)
		send_button.pack()

		#On closing
		self.top.protocol("WM_DELETE_WINDOW", self.disconnect)

		self.connect()

		try:
			tkinter.mainloop()
		except Exception as e:
			print(e)
			self.disconnect()
		
	def connect(self):
		"""Method to connect and register at the chat"""

		print('Connecting to server')

		#Creating daemon so the chat can access this object.
		daemon = Pyro4.Daemon()
		self._my_uri = daemon.register(self)

		self.t = threading.Thread(target=daemon.requestLoop)
		self.t.daemon = True
		self.t.start()

		self.api.connect_to_room(self.user.id, self.room.id)

		messages = self.chat.connect(self.my_uri)

		#in case the connection is refused:
		if isinstance(messages, bool) and not messages:
			raise ValueError(f"Username {self.username} already taken")

		print('Connected')

		#if the connection is accepted, the last 20 messages are sent
		#those messages will now be printed.
		for message in messages:
			self.incoming_message(message)

	def disconnect(self):
		"""This method closes the window and clears the username in the chat."""
		self.top.quit()
		self.chat.disconnect(self.my_uri)
		self.api.disconnect_to_room(self.user.id, self.room.id)
		print('Disconnected')

	def send_message(self, message=None):
		#Getting message from window, clearing then sending to server
		message = self.my_msg.get()
		self.my_msg.set("")
		message = f"""{self.username}: {message}"""

		self.chat.send_message(message, self.my_uri)

		#as the chat can't call methods from this object when it's called,
		#it must be printed by itself
		self.incoming_message(message)

	def incoming_message(self, message):
		#Recieving a message -> displaying at window.
		self.messages.insert(tkinter.END, message)

	def __eq__(self, other):
		return self.username == other.username

	def __str__(self):
		return self.user.username

	def __repr__(self):
		return self.user.username

	@property
	def username(self):
		return self.user.username

	@property
	def my_uri(self):
		return self._my_uri
	
	