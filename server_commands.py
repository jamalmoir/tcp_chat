import dclasses


def claim(server, client, message):
    try:
        _, username, password = message.split(" ")
    except ValueError:
        server.message_client(client=client, message=f"Invalid usage. Syntax: /claim <username> <password>")
        return

    try:
        server.users[username]
    except KeyError:
        user = dclasses.User(username=username, password=password)
        server.users[username] = user
        client.user = user
        client.nickname = user.username
        server.message_client(client=client, message=f"You have claimed the name {username}!")
    else:
        server.message_client(client=client, message=f"The name {username} is already claimed!")