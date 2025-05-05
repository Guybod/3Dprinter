import socket
import time


class URDashboardClient:
    def __init__(self, host):
        self.host = host
        self.port = 29999
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect()

    def connect(self):
        self.socket.connect((self.host, self.port))

    def send_command(self, command):
        self.socket.send(f"{command}\n".encode())
        return self.socket.recv(4096).decode()

    def close(self):
        self.socket.close()

# 使用示例
if __name__ == "__main__":
    client = URDashboardClient('192.168.1.50')  # 替换为你的机器人IP
    time.sleep(1)
    res = client.send_command("power on")
    print(res)
    time.sleep(1)
    res = client.send_command('brake release')
    time.sleep(1)

    # client.close()