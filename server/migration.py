import sys

import src.db as db


def db_up():
    connection = db.connect()
    c = connection.cursor()
    c.execute("""
    CREATE TABLE usuarios (
        id 	    number PRIMARY KEY,
        acesso  text,
        senha   text
    )
    """)
    c.execute("""
    CREATE TABLE salas (
        id              number PRIMARY KEY,
        nome            text,
        uri             text,
        dono_usuario_id number,
        modo            number,
        FOREIGN KEY (dono_usuario_id) REFERENCES usuarios (id)
    )
    """)
    c.execute("""
    CREATE TABLE usuarios_salas (
        sala_id number,
        usuario_id number,
        FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
        FOREIGN KEY (sala_id) REFERENCES salas (id) ON DELETE CASCADE
    )
    """)
    c.execute(
        """CREATE UNIQUE INDEX IF NOT EXISTS usuarios_acesso ON usuarios (acesso DESC)""")
    c.execute("""CREATE UNIQUE INDEX IF NOT EXISTS salas_uri ON salas (uri DESC)""")
    connection.commit()


def db_down():
    connection = db.connect()
    c = connection.cursor()

    c.execute('DROP INDEX IF EXISTS usuarios_acesso')
    c.execute('DROP INDEX IF EXISTS salas_uri')

    c.execute('DROP TABLE IF EXISTS usuarios_salas')
    c.execute('DROP TABLE IF EXISTS salas')
    c.execute('DROP TABLE IF EXISTS usuarios')
    connection.commit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Misisng operation argument: up, down")
        exit(1)

    op = sys.argv[1]

    if op == "up":
        db_up()
    elif op == "down":
        db_down()
    else:
        print("Invalid operation argument: up, down")
        exit(1)
