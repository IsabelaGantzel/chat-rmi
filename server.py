from src.server.server import Server

import time


if __name__=="__main__": 
	server = Server()
	server.run()

	#keeping server alive
	while True:
		time.sleep(30)
