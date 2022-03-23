from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict

import dclasses

if TYPE_CHECKING:
    from server import Server


def claim(server: Server, client: dclasses.Client, message: str):
    try:
        _, username, password = message.split(" ")
    except ValueError:
        server.message_client(
            client=client,
            message=f"Invalid usage. Syntax: /claim <username> <password>",
        )
        return

    try:
        server.users[username]
    except KeyError:
        user = dclasses.User(username=username, password=password)
        server.users[username] = user
        client.user = user
        client.nickname = user.username
        server.message_client(
            client=client, message=f"You have claimed the name {username}!"
        )
    else:
        server.message_client(
            client=client, message=f"The name {username} is already claimed!"
        )


COMMAND_MAP: Dict[str, Callable[[Server, dclasses.Client, str], None]] = {
    "claim": claim,
    "login": lambda server, client, message: None,
}
