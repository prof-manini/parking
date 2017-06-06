# -*- coding:utf-8 -*-

#
import time
from parking_simulation import SocketClient
def main(port):
    while 1:
        time.sleep(1)
        client = SocketClient(port=port)
        data = client.get_data()
        print(data)

if __name__ == "__main__":
    with open("port.txt") as file:
        port = int(file.read())
    main(port)
