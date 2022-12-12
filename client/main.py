import src.cmd as cmd
from src.api import Api


if __name__ == '__main__':
    server = 'localhost'
    port = 25500

    api = Api(server, port)
    logged_user = cmd.menu_interactive(api)
    cmd.room_interactive(api, logged_user)
