import src.cmd
import src.cmd_tk
from src.api import Api


if __name__ == "__main__":
    server = "localhost"
    port = 25500

    api = Api(server, port)
    logged_user = src.cmd_tk.menu_interactive(api)
    src.cmd_tk.room_interactive(api, logged_user)
