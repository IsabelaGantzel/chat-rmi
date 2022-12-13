import src.cmd
import src.tk_chat.cmd
from src.api import Api


if __name__ == "__main__":
    server = "localhost"
    port = 25500

    api = Api(server, port)
    logged_user = src.tk_chat.cmd.menu_interactive(api)
    src.tk_chat.cmd.room_interactive(api, logged_user)
