import struct
import time
import random
from socket import *

SERVER_IP = '127.0.0.1'
SERVER_PORT = 6501
server_address_port = (SERVER_IP, SERVER_PORT)


class Data:
    """Класс для хранения числового значения"""
    value = 0.0  # Число, которое будем передавать
    seconds = 0  # Время в секундах
    start_time = time.time()  # Засекаем стартовое время


class DataTransforms:

    @staticmethod
    def update_value(send_array):
        """Функция обновляет передаваемое значение."""
        Data.value += 0.5  # Каждую секунду увеличиваем значение на 0.5

        # Обновляем массив отправки
        send_array[2] = Data.value
        return send_array

    @staticmethod
    def update_time(send_array):
        """Обновляет время в секундах"""
        Data.seconds = int(time.time() - Data.start_time)  # Только секунды
        send_array[3] = Data.seconds  # Записываем в массив
        return send_array


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

        # Обновляем массив для отправки в зависимости от положения объекта
        send_array = DataTransforms.update_value(send_array)
        send_array = DataTransforms.update_time(send_array)

        send_array[4] = round(random.random() * 100, 3)

        # Отправляем обновленные данные
        client.send_data(send_array)
        time.sleep(1)
except KeyboardInterrupt:
    print("Программа завершена пользователем.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    UDPClientSocket.close()
