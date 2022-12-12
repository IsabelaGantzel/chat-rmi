import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class RmiChat():
	def __init__(self, name=None):
		self.name = name

	def connect(self, uri):
		"""Method for remote uses to call when wants to connect to this chat."""
		...


	def disconnect(self, uri):
		"""Method for remote uses to call when wants to disconnect from this chat."""
		...

	def send_message(self, message, uri):
		...

	def _send_message(self, message, uri=None):
		"""Method invisible for remote users due to starting with '_'.
		register the message and sends to every user connected.

		If it's a system message and must be sent to everybody, no uri is provided."""
		...
