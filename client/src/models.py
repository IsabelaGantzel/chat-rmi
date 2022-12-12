from typing import NamedTuple, List

User = NamedTuple("User", [("id", int), ("username", str), ("password", str)])
Room = NamedTuple("Room", [("id", int), ("name", str), ("uri", str), ("owner_id", int), ("mode", int)])
UserInRoom = NamedTuple("UserRoom", [("user_id", int), ("room_id", int)])
