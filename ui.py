import tkinter


class UI:
	def __init__(self, title) -> None:
		self.title = title
		self.create_ui()
	
	def create_ui(self):
		self.create_window()
		self.create_users_list()
		self.create_messages_list()
		self.create_input_message()

	def create_window(self):
		self.window = tkinter.Tk()
		self.window.title(self.title)

	def create_users_list(self):
		frame = tkinter.Frame(self.window)
		self.users_list = tkinter.Listbox(frame)
		frame.pack()

	def create_messages_list(self):
		frame = tkinter.Frame(self.window)
		scrollbar = tkinter.Scrollbar(frame)
		messages_list = tkinter.Listbox(frame, height=15, width=50, yscrollcommand=scrollbar.set)
		scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
		messages_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
		messages_list.pack()
		frame.pack()
		self.messages_list = messages_list

	def create_input_message(self):
		self.message_input = tkinter.StringVar()

		entry_field = tkinter.Entry(self.window, textvariable=self.message_input)
		entry_field.bind("<Return>", self.handle_send_button)
		entry_field.pack()

		send_button = tkinter.Button(self.window, text="Send", command=self.handle_send_button)
		send_button.pack()

	def handle_send_button(self):
		message = self.message_input.get()
		self.message_input.set("")
		self.messages_list.insert(message)

	def run(self):
		try:
			tkinter.mainloop()
		except Exception as e:
			print(e)


UI("teste").run()
