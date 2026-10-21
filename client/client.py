"""
Клиент варианта 8.
"""

from socket import *
import sys

from config import (
    SERVER_NAME,
    SERVER_PORT,
    ENCODING,
    RECV_BUFFER,
    SUPPORTED_LANGUAGES,
)


def main() -> None:
    if len(sys.argv) >= 2:
        lang = sys.argv[1].strip().lower()
    else:
        langs = "/".join(SUPPORTED_LANGUAGES)
        lang = input(f"Язык сонета ({langs}): ").strip().lower()

    if lang not in SUPPORTED_LANGUAGES:
        print(
            f"Нужно указать один из языков: {', '.join(SUPPORTED_LANGUAGES)}.")
        sys.exit(1)

    client_socket = socket(AF_INET, SOCK_STREAM)

    try:
        client_socket.connect((SERVER_NAME, SERVER_PORT))
        # одна строка с языком, затем сервер шлёт сонет
        client_socket.sendall((lang + "\n").encode(ENCODING))

        chunks = []
        while True:
            data = client_socket.recv(RECV_BUFFER)
            if not data:
                break
            chunks.append(data)

        sonnet = b"".join(chunks).decode(ENCODING)
        print("\n#Начало ответа сервера#\n")
        print(sonnet.rstrip())
        print("\n#Конец ответа сервера#\n")
    except ConnectionRefusedError:
        print("Ошибка подключения.")
        sys.exit(1)
    finally:
        client_socket.close()


if __name__ == "__main__":
    main()
