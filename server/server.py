"""
Вариант 8: TCP-сервер случайных сонетов Шекспира.
Клиент присылает язык: eng или ru.
Сервер выбирает случайный сонет из соответствующего файла и отправляет его.
"""

from socket import *
import random
from pathlib import Path

from config import (
    SERVER_HOST,
    SERVER_PORT,
    LISTEN_BACKLOG,
    ENCODING,
    CRLF_PEEK_TIMEOUT,
    SONNET_FILES,
    SUPPORTED_LANGUAGES,
    SONNET_SEPARATOR,
)


def load_sonnets(path: Path) -> list[str]:
    """Читает файл и делит сонеты по символу-разделителю."""
    text = path.read_text(encoding=ENCODING)
    parts = [
        part.strip()
        for part in text.split(SONNET_SEPARATOR)
        if part.strip()
    ]
    if not parts:
        raise ValueError(f"В файле нет сонетов: {path}")
    return parts


def recv_line(conn: socket) -> str:
    """Читает одну текстовую строку до символа перевода строки."""
    data = b""
    while True:
        chunk = conn.recv(1)
        if not chunk:
            break
        if chunk in (b"\n", b"\r"):
            # пропускаем возможный \n после \r
            if chunk == b"\r":
                conn.settimeout(CRLF_PEEK_TIMEOUT)
                try:
                    maybe_n = conn.recv(1)
                    if maybe_n and maybe_n != b"\n":
                        data += maybe_n
                except timeout:
                    pass
                finally:
                    conn.settimeout(None)
            break
        data += chunk
    return data.decode(ENCODING).strip().lower()


def main() -> None:
    # Загружаем оба набора заранее
    sonnets = {
        lang: load_sonnets(path) for lang, path in SONNET_FILES.items()
    }
    print(
        "Загружено: "
        + ", ".join(f"{lang}={len(sonnets[lang])}" for lang in SUPPORTED_LANGUAGES)
    )

    # Входной TCP-сокет (listening socket)
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(LISTEN_BACKLOG)

    print(f"Сервер готов. Порт {SERVER_PORT}. Ожидание клиентов...")

    try:
        while True:
            connection_socket, addr = server_socket.accept()
            print(f"Подключился клиент: {addr}")

            try:
                lang = recv_line(connection_socket)

                if lang not in sonnets:
                    langs = ", ".join(repr(x) for x in SUPPORTED_LANGUAGES)
                    reply = (
                        f"Ошибка: укажите язык {langs}.\n"
                        f"Получено: {lang!r}\n"
                    )
                else:
                    sonnet = random.choice(sonnets[lang])
                    reply = sonnet + "\n"
                    print(f"Отправлен сонет ({lang}) клиенту {addr}")

                connection_socket.sendall(reply.encode(ENCODING))
            except OSError as exc:
                print(f"Ошибка обмена с {addr}: {exc}")
            finally:
                connection_socket.close()
    except KeyboardInterrupt:
        print("\nОстановка сервера...")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
