import socket
import hashlib
import pyotp


def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def verify_password(password, stored_hash):
    entered_hash = hash_password(password)

    if entered_hash == stored_hash:
        return True
    else:
        return False


def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)

    return totp.verify(otp)


alice_secret = pyotp.random_base32()

users = {
    "alice": {
        "password_hash": hash_password(
            "Cyber123!"
        ),
        "totp_secret": alice_secret
    }
}


print(
    "Alice's TOTP secret:",
    users["alice"]["totp_secret"]
)

totp = pyotp.TOTP(alice_secret)

print("Current OTP:", totp.now())

server_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

server_socket.bind(
    ("127.0.0.1", 5000)
)

server_socket.listen(1)

print("Server is listening...")


client_socket, address = server_socket.accept()

print("Client connected:", address)


password_verified = False
authenticated_user = None


while True:

    message = client_socket.recv(1024).decode()

    if not message:
        break

    parts = message.split("|")


    if parts[0] == "AUTH":

        if len(parts) != 3:
            client_socket.sendall(
                "ACCESS_DENIED".encode()
            )
            continue

        username = parts[1]
        password = parts[2]

        if username not in users:
            client_socket.sendall(
                "ACCESS_DENIED".encode()
            )
            continue

        if verify_password(
            password,
            users[username]["password_hash"]
        ):

            password_verified = True
            authenticated_user = username


            client_socket.sendall(
                "OTP_REQUIRED".encode()
            )

        else:

            client_socket.sendall(
                "ACCESS_DENIED".encode()
            )


    elif parts[0] == "OTP":

        if len(parts) != 2:
            client_socket.sendall(
                "ACCESS_DENIED".encode()
            )
            continue

        if password_verified == False:
            client_socket.sendall(
                "ACCESS_DENIED".encode()
            )
            continue

        otp = parts[1]

        if verify_otp(
            users[authenticated_user]["totp_secret"],
            otp
        ):

            client_socket.sendall(
                "ACCESS_GRANTED".encode()
            )

        else:

            client_socket.sendall(
                "ACCESS_DENIED".encode()
            )


    else:

        client_socket.sendall(
            "ACCESS_DENIED".encode()
        )


client_socket.close()
server_socket.close()