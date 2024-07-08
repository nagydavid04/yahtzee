
from ftplib import FTP
import io
import re

server = FTP("???", "???", "???")
server.cwd("yahtzee")


def validate_username(username, accounts):
    TAB = "     "
    if username in accounts.keys():
        return "Username is already used!"
    elif username == TAB:
        return "Please enter a username!"
    return False


def validate_email(email, accounts):
    TAB = "     "
    if email == TAB:
        return "Please enter an e-mail address!"

    for val in accounts.values():
        if val["email"] == email:
            return "E-mail already used!"

    pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return "Please enter a valid e-mail address!"

    return False


def validate_password(pass1, pass2):
    TAB = "     "
    if pass1 == TAB:
        return "Please enter a password!"

    if pass1 != pass2:
        return "Passwords don't match!"

    if len(pass1) < 8:
        return "Please enter a longer password!"

    return False


def list_dir():
    files = server.nlst()

    files.remove(".")
    files.remove("..")

    return files


def download_accounts():
    datas = []
    server.retrbinary("RETR accounts.txt", datas.append)

    accounts = eval(datas[0].decode())

    return accounts


def upload_accounts(accounts):
    accounts = str(accounts)
    byte_data = accounts.encode("utf-8")
    file_like_object = io.BytesIO(byte_data)

    server.storbinary("STOR accounts.txt", file_like_object)


def download_online_players_status():
    datas = []
    server.retrbinary("RETR online_players_status.txt", datas.append)

    online_players_status = eval(datas[0].decode())

    return online_players_status


def upload_online_players_status(online_players_status):
    online_players_status = str(online_players_status)
    byte_data = online_players_status.encode("utf-8")
    file_like_object = io.BytesIO(byte_data)

    server.storbinary("STOR online_players_status.txt", file_like_object)


def download_requests():
    server.cwd("requests")

    files = list_dir()
    datas = []

    while len(datas) != len(files):
        datas = []
        for file in files:
            server.retrbinary(f"RETR {file}", datas.append)

    for file in files:
        server.delete(file)

    server.cwd("..")

    return [[file.split("%%%")[:-1], datas[i].decode("utf-8").split("%%%")[:-1]] for i, file in enumerate(files)]


def upload_responses(responses):
    server.cwd("responses")
    for name_command, response in responses:
        server.storbinary(f"STOR {name_command[0]}%%%{name_command[1]}%%%", io.BytesIO(response.encode("utf-8")))
    server.cwd("..")


def handle_request_register(request, accounts):
    username, email, password1, password2 = request

    ret = validate_username(username, accounts)
    if ret:
        return ret

    ret = validate_email(email, accounts)
    if ret:
        return ret

    ret = validate_password(password1, password2)
    if ret:
        return ret

    accounts[username] = {}
    accounts[username]["password"] = password1
    accounts[username]["email"] = email

    return "Done!"


def handle_request_login(request, accounts, online_players_status):
    TAB = "     "
    username, password = request

    if username == TAB:
        return "Please enter a username!"

    elif username not in accounts.keys():
        return "Username is not registered!"

    if password == TAB:
        return "Please enter the password!"

    elif accounts[username]["password"] != password:
        return "Password is incorrect!"

    online_players_status[username] = {}
    online_players_status[username]["searching"] = False
    online_players_status[username]["invite"] = None
    online_players_status[username]["in_match"] = False

    return "Done!"


def handle_modify_status(request, online_players_status):
    username, searching, invite, in_match = request

    online_players_status[username] = {}
    online_players_status[username]["searching"] = True if searching == "True" else False
    online_players_status[username]["invite"] = None if invite == "None" else invite
    online_players_status[username]["in_match"] = True if in_match == "True" else False


def handle_upload_game_variables(request):
    path, game_variables = request

    server.cwd("matches")

    server.storbinary(f"STOR {path}", io.BytesIO(game_variables.encode("utf-8")))

    server.cwd("..")


def handle_download_game_variables(request):
    path = request[0]

    server.cwd("matches")

    data = []
    server.retrbinary(f"RETR {path}", data.append)

    server.cwd("..")

    game_variables = data[0].decode()

    return game_variables


while True:
    accounts = None
    online_players_status = None

    requests = download_requests()
    responses = []

    for name_command, parameters in requests:
        command = name_command[1]
        if command != "get_online_players_status" or "download_game_variables":
            print(f"Command: {command}, parameters: {parameters}")
        need_response = True if parameters[-1] == "True" else False
        parameters = parameters[:-1]

        response = None

        if command == "register":
            try:
                if accounts is None:
                    accounts = download_accounts()

                response = [name_command, handle_request_register(parameters, accounts)]

            except Exception as e:
                print(e)

        elif command == "login":
            try:
                if accounts is None:
                    accounts = download_accounts()

                if online_players_status is None:
                    online_players_status = download_online_players_status()

                response = [name_command, handle_request_login(parameters, accounts, online_players_status)]

            except Exception as e:
                print(e)

        elif command == "get_online_players_status":
            try:
                if online_players_status is None:
                    online_players_status = download_online_players_status()

                response = [name_command, str(online_players_status)]

            except Exception as e:
                print(e)

        elif command == "modify_status":
            try:
                if online_players_status is None:
                    online_players_status = download_online_players_status()

                handle_modify_status(parameters, online_players_status)
                response = [name_command, "Done!"]
            except Exception as e:
                print(e)

        elif command == "remove_status":
            try:
                if online_players_status is None:
                    online_players_status = download_online_players_status()

                online_players_status.pop(parameters[0])
                response = [name_command, "Done!"]

            except Exception as e:
                print(e)

        elif command == "upload_game_variables":
            try:
                handle_upload_game_variables(parameters)
                response = [name_command, "Done!"]

            except Exception as e:
                print(e)

        elif command == "download_game_variables":
            try:
                response = [name_command, handle_download_game_variables(parameters)]

            except Exception as e:
                print(e)

        if need_response:
            responses.append(response)

    if accounts is not None:
        try:
            upload_accounts(accounts)

        except Exception as e:
            print(e)

    if online_players_status is not None:
        try:
            upload_online_players_status(online_players_status)

        except Exception as e:
            print(e)

    try:
        upload_responses(responses)

    except Exception as e:
        print(e)
