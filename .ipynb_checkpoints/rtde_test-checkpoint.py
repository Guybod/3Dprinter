from rtde_control import Path, PathEntry
import json
import requests
import time
from split_script import split_script

url = "http://192.168.1.103:7125/printer/gcode/script?include_monitors=false"
# robot IP
ROBOT_IP = "192.168.1.50"
# robot速度(m/s)
speed_ms = 0.02
# robot加速度
accel_mss = 3.0
# robot交融半径m
blend_radius_m = 0.001

# UR控制端对象
rtde_C = None
# UR接收端对象
rtde_r = None

# 创建path对象
path = Path()

global Data


# 发送脚本请求
def extruder(script):
    payload = json.dumps({
        "script": script
    })
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json',
        'Accept': '*/*',
        'Host': '192.168.1.103:7125',
        'Connection': 'keep-alive'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def split_move_path(move_path):
    movement_dict = split_script(move_path)
    final_path = Path()

    for key, value in movement_dict.items():
        new_path_paramers = []
        new_path_paramers.extend(value[1][:6])
        parts = value[2].split(',')
        if len(parts) > 0 and parts[0] == "accel_mss":
            new_path_paramers.append(accel_mss)
        if len(parts) > 1 and parts[1] == "speed_ms":
            new_path_paramers.append(speed_ms)
        if len(parts) > 2 and parts[2] == "0":
            new_path_paramers.append(0)
        if len(parts) > 3 and parts[3] == "0.0000":
            new_path_paramers.append(0.0000)
        if len(parts) > 3 and parts[3] == "blend_radius_m":
            new_path_paramers.append(blend_radius_m)

        # 假设 PathEntry 用于创建路径点
        path_entry = PathEntry(new_path_paramers)
        final_path.addEntry(path_entry)

    return final_path


if __name__ == "__main__":
    path = split_move_path('script.txt')
    # 假设 Path 类有获取路径点数量的方法
    for i in range(path.size()):
        entry = path.getEntry(i)
        print(entry.getParameters())

    # extruder("M83")
    # print("send M83")
    # time.sleep(0.5)
    # extruder("G1 F300")
    # print("send G1 F300")

    # try:
    #     import rtde_control
    #
    #     rtde_C = rtde_control.RTDEControlInterface(ROBOT_IP)
    #     if rtde_C.isConnected():
    #         print("connected!")
    #     print("move")
    #     # 假设 Path 类有转换为列表的方法
    #     path_list = []
    #     for i in range(path.size()):
    #         entry = path.getEntry(i)
    #         path_list.append(entry.getParameters())
    #     rtde_C.moveL(path_list, True)
    #
    #     signal = True
    #     Data = 0
    #     while signal:
    #         data = rtde_C.getAsyncOperationProgress()
    #         if Data != data:
    #             extruder("G1 E10 F300")
    #             print(data)
    #             Data = data
    #         if data < 0:
    #             signal = False
    # except ImportError:
    #     print("rtde_control 模块未找到，请检查安装情况。")
