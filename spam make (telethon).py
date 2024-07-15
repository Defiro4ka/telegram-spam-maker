import os
import asyncio
import logging
from telethon import TelegramClient
from telethon.errors import ChatForbiddenError

# Установка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Логотип
logo = """
    ░██████╗██████╗░░█████╗░███╗░░░███╗
    ██╔════╝██╔══██╗██╔══██╗████╗░████║
    ╚█████╗░██████╔╝███████║██╔████╔██║
    ░╚═══██╗██╔═══╝░██╔══██║██║╚██╔╝██║
    ██████╔╝██║░░░░░██║░░██║██║░╚═╝░██║
    ╚═════╝░╚═╝░░░░░╚═╝░░╚═╝╚═╝░░░░░╚═╝

        ███╗░░░███╗░█████╗░██╗░░██╗███████╗██████╗░
        ████╗░████║██╔══██╗██║░██╔╝██╔════╝██╔══██╗
        ██╔████╔██║███████║█████═╝░█████╗░░██████╔╝
        ██║╚██╔╝██║██╔══██║██╔═██╗░██╔══╝░░██╔══██╗
        ██║░╚═╝░██║██║░░██║██║░╚██╗███████╗██║░░██║
        ╚═╝░░░░░╚═╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝╚═╝░░╚═╝ by ???
"""
print(logo)

# Функция для получения пользовательского ввода
def get_input(prompt, validate):
    while True:
        value = input(prompt)
        if validate(value):
            return value
        print("Invalid input.")

# Получение параметров от пользователя
s1 = int(get_input("Please enter spam cycles: ", lambda x: x.isdigit() and int(x) != 0))
s2 = get_input("Please enter folder with telegram session: ", lambda x: os.path.isdir(x) and any(os.listdir(x)))
use_proxy = input("Do you want to use a proxy? (yes/no): ").strip().lower() == 'yes'
if use_proxy:
    proxy_file = get_input("Please enter the path to the proxy file: ", lambda x: os.path.isfile(x) and os.path.getsize(x) > 0)
else:
    proxy_file = None
    print("Proxy will not be used.")
chat_id = int(get_input("Please enter the chat ID: ", lambda x: x.isdigit()))
print(f"Chat ID '{chat_id}' will be used for sending.")
delay = int(get_input("Please enter the delay between messages in milliseconds: ", lambda x: x.isdigit() and int(x) >= 0))
print(f"Delay set to {delay} milliseconds.")

# Функция для получения клиента Telegram
def get_client(session_file):
    api_id =  # Используйте ваш api_id
    api_hash = '' # Используйте ваш api_hash
    return TelegramClient(session_file, api_id, api_hash)

# Функция для отправки сообщений
async def send_messages(client, chat_id, delay):
    try:
        async with client:
            await client.start()
            logger.info(f"Client {client.session.filename} started")

            for i in range(s1):
                await client.send_message(chat_id, "i ♥ u") # Сообщение для отправки
                logger.info(f"Message {i+1}/{s1} sent to {chat_id}")
                await asyncio.sleep(delay / 1000)
    except ChatForbiddenError:
        logger.error(f"Access to chat {chat_id} is forbidden.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")

# Основная функция для запуска всех клиентов
async def main():
    session_files = [os.path.join(s2, f) for f in os.listdir(s2) if f.endswith('.session')]
    clients = [get_client(session_file) for session_file in session_files]
    tasks = [send_messages(client, chat_id, delay) for client in clients]
    await asyncio.gather(*tasks)

# Запуск основной функции
asyncio.run(main())
