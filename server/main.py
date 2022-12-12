from src.server import Server

import time

if __name__ == "__main__":
    # ='192.168.100.20'
    hostname = 'localhost'
    port = 25500
    lobby_port = 25501
    server = Server(hostname=hostname, port=port, lobby_port=lobby_port)
    server.run()

    # keeping server alive
    while True:
        time.sleep(30)
