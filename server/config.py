from pathlib import Path

# Адрес и порт, на которых слушает сервер
SERVER_HOST = ""
SERVER_PORT = 12000
LISTEN_BACKLOG = 1     # размер очереди ожидающих соединений

# Кодировка текстового обмена
ENCODING = "utf-8"

# Таймаут при разборе \r\n (секунды)
CRLF_PEEK_TIMEOUT = 0.05

# Поддерживаемые языки и файлы с сонетами
BASE_DIR = Path(__file__).resolve().parent
SONNET_FILES = {
    "eng": BASE_DIR / "sonnets_eng.txt",
    "ru": BASE_DIR / "sonnets_ru.txt",
}
SUPPORTED_LANGUAGES = tuple(SONNET_FILES.keys())

# Разделитель сонетов в файле
SONNET_SEPARATOR = "#"
