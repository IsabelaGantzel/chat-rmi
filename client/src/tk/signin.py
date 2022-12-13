import tkinter as tk
from tkinter import ttk


class TkSignin(tk.Tk):
    def __init__(self):
        super().__init__()
        self.declare_events()
        self.create_ui()

    def declare_events(self):
        self.on_submit = None

    def create_ui(self):
        self.geometry("240x100")
        self.title("Entrar")
        self.resizable(0, 0)

        # configure the grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        self.create_widgets()

        self.username_entry.focus()

    def create_widgets(self):
        # username
        username_label = ttk.Label(self, text="Usuário:")
        username_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)

        self.username_entry = ttk.Entry(self)
        self.username_entry.bind("<Return>", lambda _event: self.password_entry.focus())
        self.username_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)

        # password
        password_label = ttk.Label(self, text="Senha:")
        password_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)

        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.bind("<Return>", lambda _event: self.handle_submit())
        self.password_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)

        # login button
        login_button = ttk.Button(self, text="Entrar", command=self.handle_submit)
        login_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

    def handle_submit(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        self.on_submit(username, password)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    # Example

    def on_submit(username, password):
        print(f"username: {username}")
        print(f"password: {password}")

    app = TkSignin()
    app.on_submit = on_submit
    app.run()
