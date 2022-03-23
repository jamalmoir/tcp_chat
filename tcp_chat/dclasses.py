import dataclasses
from typing import Any, Optional


@dataclasses.dataclass
class User:
    username: str
    password: str
    level: int = 3


@dataclasses.dataclass
class Client:
    client: Any
    address: str
    nickname: str
    user: Optional[User] = None
