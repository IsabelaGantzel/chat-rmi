import sqlite3
from .models import User, Room, UserInRoom


def connect():
    return sqlite3.connect("database.db")


# Users


def get_next_user_id():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM usuarios")
    (result,) = cursor.fetchone()
    result = result or 0
    return result + 1


def register_user(username: str, password: str):
    connection = connect()
    cursor = connection.cursor()
    id = get_next_user_id()
    args = [id, username, password]
    cursor.execute("INSERT INTO usuarios (id, acesso, senha) VALUES (?, ?, ?)", args)
    connection.commit()
    return get_user_by_id(id)


def get_user(username: str):
    connection = connect()
    cursor = connection.cursor()
    args = [username]
    cursor.execute("SELECT * FROM usuarios WHERE acesso = ?", args)
    result = cursor.fetchone()
    return User(*result) if result is not None else None


def get_user_by_id(id: int):
    connection = connect()
    cursor = connection.cursor()
    args = [id]
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", args)
    result = cursor.fetchone()
    return User(*result) if result is not None else None


def clean_users():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM usuarios")
    connection.commit()


# Rooms


def get_rooms():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM salas")
    result = cursor.fetchall()
    return [Room(*it) for it in result]


def get_next_room_id():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("SELECT MAX(id) FROM salas")
    (result,) = cursor.fetchone()
    result = result or 0
    return result + 1


def get_room_by_id(id: int):
    connection = connect()
    cursor = connection.cursor()
    args = [id]
    cursor.execute("SELECT * FROM salas WHERE id = ?", args)
    result = cursor.fetchone()
    return Room(*result) if result is not None else None


def register_room(user_id: int, name: str, uri: str, mode: int):
    connection = connect()
    cursor = connection.cursor()
    id = get_next_room_id()
    args = [id, name, uri, user_id, mode]
    cursor.execute(
        "INSERT INTO salas (id, nome, uri, dono_usuario_id, modo) VALUES (?, ?, ?, ?, ?)",
        args,
    )
    connection.commit()
    return get_room_by_id(id)


def user_is_owner_or_room(user_id: int, room_id: int):
    result = get_room_by_id(room_id)
    if result is None:
        return None
    if result.owner_id != user_id:
        return None
    return Room(*result)


def remove_room(id: int):
    connection = connect()
    cursor = connection.cursor()
    args = [id]
    cursor.execute("DELETE FROM salas WHERE id = ?", args)
    connection.commit()
    return cursor.rowcount


def clean_rooms():
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM salas")
    connection.commit()


# Users In Rooms


def remove_user_in_room(user_id: int, room_id: int) -> int:
    connection = connect()
    cursor = connection.cursor()
    args = [room_id, user_id]
    cursor.execute(
        "DELETE FROM usuarios_salas WHERE sala_id = ? AND usuario_id = ?", args
    )
    connection.commit()
    return cursor.rowcount


def register_user_in_room(user_id: int, room_id: int):
    connection = connect()
    cursor = connection.cursor()
    args = [room_id, user_id]
    cursor.execute(
        "INSERT INTO usuarios_salas (sala_id, usuario_id) VALUES (?, ?)", args
    )
    connection.commit()


def get_user_rooms(user_id: int):
    connection = connect()
    cursor = connection.cursor()
    args = [user_id]
    cursor.execute("SELECT * from usuarios_salas WHERE usuario_id = ?", args)
    result = cursor.fetchall()
    return [UserInRoom(*it) for it in result]


def get_room_users(room_id: int):
    connection = connect()
    cursor = connection.cursor()
    args = [room_id]
    cursor.execute("SELECT * from usuarios_salas WHERE sala_id = ?", args)
    result = cursor.fetchall()
    return [UserInRoom(*it) for it in result]
