# Get started

```bash
# Instalação das dependencias
pip3 install -r requirements.txt

# Criar e inicializar o banco de dados
python3 migration.py up

# Executar o servidor
python3 server.py

# Executar o cliente
python3 client.py
```


# RMI-Chat

Chat coded in python using RMI

Programming language: Python 3.7.0

Used libraries:
	- json
	- time
	- socket
	- threading
	- tkinter
	- Pyro4

Pyro4 and tkinter might not come with your python version, depending on the operation system and/or python distribution.

The program consists in 4 files:
	- client.py - responsable for discovering the existing chats in the server and connecting the user to the chat room.
	- server.py - responsable for creating a 'dns server' to locate the uri and start the chat rooms.
	- user.py - contains the 'User' class which will create a GUI and interact with the chatroom via RMI.
	- chat.py - contains the 'Chat' class which manages the interations between the connected users.


In case no python 3.7 nor one of the libraries are installed in your machine, you may enter the 'server' and 'client' folders to execute the .exe files to verify it's functionalities.

The .exe versions were created using the pyinstall library.

In this version of the file server.exe, only 3 rooms are created.

# Requisitos

Você foi contratado para o desenvolvimento de um sistema para comunicação interpessoal: o WhatsUT. Tal sistema precisa atender os seguintes requisitos:

1) [OK] Autenticação criptografada: o usuário precisa estar cadastrado para utilizar, e seu acesso deve ser feito via senha. É importante usar um processo de criptografia de dados.

2) [OK] Lista de usuários: ao realizar o login, uma lista de usuários deve ser apresentada, caracterizando o usuário que estiver atualmente logado e disponível para chat.

3) [OK] Lista de grupos: uma lista de grupos para chat deve ser apresentada. O cliente poderá pedir para entrar no grupo de conversa, sendo aprovado ou não pelo criador do grupo de conversação.

3) Dois modos de chat devem ser providos: chat privado, permitindo a conversação entre duas pessoas apenas; e chat em grupo, permitindo com que várias pessoas possam se juntar a uma conversa. No caso da conversa em grupo, o usuário que criou pode dar permissão a outros usuários para entrada.

5) Envio de arquivos: em chats privados, um usuário poderá enviar arquivos ao outro usuário.

6) [OK] Exclusão: um usuário poderá requisitar ao servidor que um usuário seja banido da aplicação. Banir um usuário do grupo é tarefa do administrador do grupo. Caso o administrador do grupo saia, o aplicativo deve decidir quem será o novo administrador, ou se o grupo seja eliminado. Tal opção pode ser ajustada no momento da criação do chat em grupo. 

É importante que se tenha telas intuitivas, modernas e "caprichadas" tanto para o cliente quanto para o servidor. Ainda, deve-se apresentar os diagramas UML (atividades, sequencia e classes).
