import rtde_control
from rebuild.read_config import get_config

print("正在连接...")
IP = get_config("ROBOT_IP")
print(f"原始IP: {IP!r}")  # 显示原始字符串内容，查看是否有隐藏字符
IP = IP.strip()  # 去除首尾空格/换行
print()
rtde_c = rtde_control.RTDEControlInterface(IP)
if rtde_c.isConnected():
    print("连接成功")
else:
    print("连接失败")
