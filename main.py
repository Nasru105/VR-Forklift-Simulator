import struct
import time
import random
from socket import *

SERVER_IP = '127.0.0.1'
SERVER_PORT = 6501
server_address_port = (SERVER_IP, SERVER_PORT)


class Client:
    @staticmethod
    def send_data(array):
        """Отправка данных в VR Concept """
        UDPClientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
        bts = [struct.pack('d', f) for f in array]
        UDPClientSocket.sendto(b''.join(bts), server_address_port)

    @staticmethod
    def get_data(UDPClientSocket):
        """Получение данных из VR Concept """
        buffer_size = 1024  # Paзмеp бyoеpa
        conn, _ = UDPClientSocket.recvfrom(buffer_size)

        try:
            array = struct.unpack('10d', conn[:80])  # Гарантируем, что берём только первые 80 байтов
        except struct.error as e:
            print(f"Ошибка распаковки: {e}, получено {len(conn)} байтов")
            array = [0.0] * 10  # Возвращаем массив с нулями

        return array


try:
    UDPClientSocket = socket(family=AF_INET, type=SOCK_DGRAM)
    UDPClientSocket.bind(('127.0.0.1', 6502))  # Порт для получения данных
    client = Client()
    send_array = [0 for _ in range(10)]  # массив для отправки данных

    while True:
        get_array = client.get_data(UDPClientSocket)  # Получаем данные от VR Concept

        send_array[0] += 0.001  # смещение по оси х
        send_array[1] += 0.001  # смещение по оси z
        send_array[2] -= 0.2  # угол поворота
        send_array[3] = random.randint(1, 10 ** 8) * 0.001

        # Отправляем обновленные данные
        client.send_data(send_array)
        time.sleep(0.001)
except KeyboardInterrupt:
    print("Программа завершена пользователем.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    UDPClientSocket.close()
