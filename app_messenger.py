import socket
import threading
import sys

# Настройки клиента
host = "95.165.169.101"
port = 4567

# Функция для отправки сообщений
def send_message(client_socket):
    while True:
        message = input('Отправьте сообщение: ')
        client_socket.send(message.encode('utf-8'))

# Функция для получения сообщений
def receive_message(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Перемещаем курсор в начало строки и выводим полученное сообщение на новой строке
                print(f"\rПолучено сообщение: {message}\nОтправьте сообщение: ", end='', flush=True)
        except:
            print("[!] Ошибка при получении сообщения")
            client_socket.close()
            break

# Функция для запуска клиента
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Запуск потоков для отправки и получения сообщений
    threading.Thread(target=send_message, args=(client_socket,)).start()
    threading.Thread(target=receive_message, args=(client_socket,)).start()

if __name__ == "__main__":
    start_client()
