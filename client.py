import src.client.cmd as cmd
from src.client.api import Api

import json
import socket as sk


def main(server='192.168.100.20', port=25500):
	api = Api(server, port)
	logged_user = cmd.menu_interactive(api)
	cmd.room_interactive(api, logged_user)


if __name__ == '__main__':
	main()