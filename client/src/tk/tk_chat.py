import tkinter as tk

BG = "#e8eaf6"

CONTAINER_BG = "#e8eaf6"

LABEL_CONFIG = dict(bg="#bbdefb")

SEND_MESSAGE_CONFIG = dict(
    bg="#bbdefb",
    activebackground="#bbdefb",
    highlightbackground="#bbdefb",
)

SEND_FILE_CONFIG = dict(
    bg="#f8bbd0",
    activebackground="#f8bbd0",
    highlightbackground="#f8bbd0",
)

MESSAGES_LIST_CONFIG = dict(
    bg=CONTAINER_BG,
)

USERS_LIST_CONFIG = dict(
    bg=CONTAINER_BG,
)


class TkChat:
    def __init__(self, admin) -> None:
        super().__init__()
        self.selected_index = None
        self.running = False
        self.admin = admin

        self.declare_events()
        self.create_ui()

    def declare_events(self):
        self.on_send_message = None
        self.on_send_file = None
        self.on_close = None
        self.on_delete = None

    def create_ui(self):
        self.root = tk.Tk()
        self.root.geometry("600x500")
        self.root.configure()

        self.grid_rows_columns(10, 12)
        self.configure_layout((9, 4), (9, 8))

        users_list_label = tk.Label(self.left, text="Users")
        users_list_label.configure(**LABEL_CONFIG)
        users_list_label.pack(fill=tk.BOTH)

        user_list_scroll = tk.Scrollbar(self.left)
        self.users_list = tk.Listbox(
            self.left, yscrollcommand=user_list_scroll.set, **USERS_LIST_CONFIG
        )
        self.users_list.bind("<<ListboxSelect>>", self.handle_user_select)
        self.users_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        user_list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        message_list_label = tk.Label(self.right, text="Messages")
        message_list_label.configure(**LABEL_CONFIG)
        message_list_label.pack(fill=tk.BOTH)

        message_list_scroll = tk.Scrollbar(self.right)
        self.messages_list = tk.Listbox(
            self.right, yscrollcommand=message_list_scroll.set, **MESSAGES_LIST_CONFIG
        )
        self.messages_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        message_list_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.message_input = tk.StringVar()
        self.message_field = tk.Entry(self.bottom, textvariable=self.message_input)
        self.message_field.bind("<Return>", lambda _event: self.handle_send_button())
        self.message_field.pack(
            side=tk.LEFT,
            fill=tk.X,
            expand=1,
            padx=(5, 0),
            pady=5,
            ipadx=5,
            ipady=5,
        )

        if self.admin:
            self.delete_button = tk.Button(
                self.bottom,
                text="Deletar",
                padx=5,
                pady=3,
                command=self.handle_delete_button,
            )
            self.delete_button.configure(SEND_FILE_CONFIG)
            self.delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.send_file_button = tk.Button(
            self.bottom,
            text="Enviar arquivo",
            padx=5,
            pady=3,
            command=self.handle_send_file_button,
        )
        self.send_file_button.configure(SEND_FILE_CONFIG)
        self.send_file_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.send_message_button = tk.Button(
            self.bottom,
            text="Enviar",
            padx=5,
            pady=3,
            command=self.handle_send_button,
        )
        self.send_message_button.configure(**SEND_MESSAGE_CONFIG)
        self.send_message_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.users_list.insert(tk.END, "<Todos>")

        self.root.protocol("WM_DELETE_WINDOW", self.handle_close)

    def grid_columns(self, n: int) -> None:
        for i in range(n):
            self.root.columnconfigure(i, weight=1)

    def grid_rows(self, n: int) -> None:
        for i in range(n):
            self.root.rowconfigure(i, weight=1)

    def grid_rows_columns(self, rows: int, columns: int) -> None:
        self.grid_rows(rows)
        self.grid_columns(columns)

    def configure_layout(self, left, right):
        config = dict(
            row=0, column=0, rowspan=left[0], columnspan=left[1], sticky="nsew"
        )
        self.left = tk.Frame(self.root)
        self.left.grid(**config, padx=(5, 0), pady=5)

        config["row"] = 0
        config["column"] = config["columnspan"]
        config["rowspan"] = right[0]
        config["columnspan"] = right[1]
        self.right = tk.Frame(self.root)
        self.right.grid(**config, padx=5, pady=5)

        config["row"] = left[0]
        config["column"] = 0
        config["rowspan"] = 1
        config["columnspan"] = 12
        self.bottom = tk.Frame(self.root)
        self.bottom.grid(**config, padx=5, pady=(0, 5))

    def handle_close(self):
        if self.on_close is not None:
            self.on_close()
        self.root.quit()

    def handle_send_button(self):
        if self.on_send_message is None:
            return

        username = self.get_selected_user()
        message = self.message_input.get()
        if message != "":
            self.message_input.set("")
            self.on_send_message(username, message)

    def get_selected_user(self):
        if self.selected_index is not None:
            index = self.selected_index
            username = self.users_list.get(index)
            return username.strip("<>")

    def handle_send_file_button(self):
        if self.on_send_file is None:
            return

        selected_user = self.get_selected_user()
        if selected_user is not None:
            self.on_send_file(selected_user)

    def handle_delete_button(self):
        if self.on_delete is None:
            return

        selected_user = self.get_selected_user()
        if selected_user is not None:
            self.on_delete(selected_user)

    def get_user_list(self):
        return [it.strip("<>") for it in self.users_list.get(0, tk.END)]

    def handle_user_select(self, event):
        widget = event.widget
        index = next(iter(widget.curselection()), None)

        if index is not None:
            self.selected_index = index if index != 0 else None

            items = self.get_user_list()
            for i, it in enumerate(items):
                self.users_list.delete(i)

                if i == index:
                    it = f"<{it}>"

                self.users_list.insert(i, it)

    def add_message(self, message: str):
        self.messages_list.insert(tk.END, message)

    def add_user(self, user: str):
        self.users_list.insert(tk.END, user)

    def remove_user(self, user: str):
        index = self.get_user_list().index(user)
        self.users_list.delete(index)

    def set_title(self, title: str):
        self.root.title(title)

    def run(self):
        self.running = True
        try:
            self.root.mainloop()
        except Exception as e:
            self.handle_close()
            raise e
        finally:
            self.running = False


if __name__ == "__main__":

    def on_send_message(user, message):
        print(user, message)

    def on_send_file(user):
        print("File", user)

    def on_delete(user):
        print("Deletar", user)

    def on_close():
        print("Close")

    app = TkChat()

    app.on_send_message = on_send_message
    app.on_send_file = on_send_file
    app.on_close = on_close
    app.on_delete = on_delete

    app.add_message("Hello")
    app.add_message("World")
    app.add_user("User 1")
    app.add_user("User 2")

    app.run()
