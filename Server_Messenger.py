import socket
import threading

# Настройки сервера
HOST = '192.168.2.66'  # Сервер доступен для всех устройств в сети
PORT = 4567
clients = []

# Функция для отправки аудио всем клиентам, кроме источника
def broadcast(data, exclude_socket=None):
    for client in clients:
        sock = client[1]
        if sock != exclude_socket:
            try:
                sock.sendall(data)
            except Exception as e:
                print(f"Ошибка отправки данных клиенту: {e}")
                clients.remove(client)

# Обработка клиента
def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(320)  # Получаем аудиоданные
            if not data:
                break
            broadcast(data, exclude_socket=client_socket)  # Отправляем другим клиентам
        except Exception as e:
            print(f"Ошибка клиента: {e}")
            break

    # Закрытие соединения
    clients.remove((client_socket,))
    client_socket.close()
    print(f"Клиент отключен")

# Запуск сервера
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Клиент {addr} подключен")
        clients.append((addr, client_socket))
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
