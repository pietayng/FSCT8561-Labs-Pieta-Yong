import socket
from getpass import getpass


client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

client_socket.connect(
    ("127.0.0.1", 5000)
)


username = input("Username: ")
password = getpass("Password: ")


message = "AUTH|" + username + "|" + password

client_socket.sendall(
    message.encode()
)


response = client_socket.recv(1024).decode()

print(response)


if response == "OTP_REQUIRED":

    otp = input("OTP: ")

    message = "OTP|" + otp

    client_socket.sendall(
        message.encode()
    )

    response = client_socket.recv(1024).decode()

    print(response)


client_socket.close()