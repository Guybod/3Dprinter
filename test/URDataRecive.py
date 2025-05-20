import socket
import struct
import threading
import time
import queue

class URDataParser:
    # 共享数据结构（作为嵌套类）
    class UR_Stream_Data:
        J_Orientation = [0.0] * 6  # 关节角度（保留原字段）
        TCP_Speed = [0.0] * 6      # TCP 速度（新增）

    def __init__(self, server_ip, port=30003):
        self.server_ip = server_ip
        self.port = port
        self.client_socket = None
        self.is_running = False

        # 线程安全队列（保留最新数据）
        self.speed_queue = queue.Queue(maxsize=1)

        # 创建数据实例
        self.ur_data = self.UR_Stream_Data()

        # 连接参数
        self.reconnect_interval = 2
        self.buffer_size = 1220  # UR RTDE 包大小

    def connect(self):
        """建立TCP连接并启动接收线程"""
        self.is_running = True
        self.receive_thread = threading.Thread(target=self._receive_data, daemon=True)
        self.receive_thread.start()

    def _reconnect(self):
        """断线重连机制"""
        while self.is_running:
            try:
                print("尝试重新连接...")
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.settimeout(5)
                self.client_socket.connect((self.server_ip, self.port))
                print("重新连接成功")
                return
            except Exception as e:
                print(f"连接失败: {str(e)}")
                time.sleep(self.reconnect_interval)

    def _receive_data(self):
        """数据接收线程主循环"""
        while self.is_running:
            try:
                if not self.client_socket:
                    self._reconnect()
                    continue

                # 读取完整数据包
                data = bytearray()
                while len(data) < self.buffer_size:
                    chunk = self.client_socket.recv(self.buffer_size - len(data))
                    if not chunk:
                        raise ConnectionError("连接已关闭")
                    data.extend(chunk)

                # 解析TCP速度
                tcp_speed = self._parse_tcp_speed(data)

                # 更新队列（替换旧数据）
                if self.speed_queue.full():
                    self.speed_queue.get_nowait()
                self.speed_queue.put(tcp_speed)

            except (ConnectionError, socket.error) as e:
                print(f"接收数据错误: {str(e)}")
                self.client_socket = None
                self._reconnect()
            except Exception as e:
                print(f"未知错误: {str(e)}")
                self.close()

    def _parse_tcp_speed(self, packet):
        """
        解析TCP速度数据
        packet: bytes 原始数据包
        返回: list[float] TCP速度 [vx, vy, vz, wx, wy, wz]
        """
        if len(packet) < 891:  # 根据UR协议 tcp_speed偏移为843，每个double占8字节，共6个字段
            raise ValueError("数据包长度不足")

        offset = 843  # tcp_speed 起始偏移量（根据协议版本可能不同）
        speed = []

        for i in range(6):
            (value,) = struct.unpack_from('>d', packet, offset + i * 8)
            speed.append(round(value, 3))  # 保留三位小数

        return speed

    def update(self):
        """主循环中调用以更新数据"""
        try:
            # 获取最新数据（非阻塞）
            latest_speed = self.speed_queue.get_nowait()
            self.ur_data.TCP_Speed = latest_speed
        except queue.Empty:
            pass  # 无新数据时跳过

    def close(self):
        """关闭连接"""
        self.is_running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
        # 不要 join 自己所在的线程
        if threading.current_thread() != self.receive_thread:
            self.receive_thread.join(timeout=1)


# 使用示例
if __name__ == "__main__":
    parser = URDataParser("192.168.106.128")  # 替换为实际IP
    parser.connect()

    # 打开文件用于写入
    with open("tcpSpeed.txt", "w") as f:
        try:
            while True:
                # 在主循环中更新数据
                parser.update()

                # 获取当前TCP速度
                speed = parser.ur_data.TCP_Speed
                print(f"当前TCP速度: {speed}")

                # 将速度写入文件
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {speed}\n")
                f.flush()  # 立即写入磁盘

                time.sleep(0.1)  # 控制输出频率
        except KeyboardInterrupt:
            parser.close()
