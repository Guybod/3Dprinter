import time

import rtde_control
import rtde_receive
from threading import Thread

speed_ms = 0.02
# robot加速度
accel_mss = 3.0
# robot交融半径m
blend_radius_m = 0.001

signal = True

now_position = []

ROBOT_IP = '192.168.1.50'

def split_script(script_path):
    # 用于存储最终结果的字典，键为递增数字，值为包含移动指令、参数和挤出机值的列表
    movement_dict = {}
    # 用于记录Extruder后面的值，初始化为0
    extruder_value = 0
    # 用于生成递增的数字键，初始化为1
    index = 1
    movepath =[]

    with open(script_path, 'r') as file:
        # 读取文件的所有行
        lines = file.readlines()
        for i in range(len(lines)):
            # 去除每行两端的空白字符
            line = lines[i].strip()
            if line.startswith('Extruder'):
                # 提取Extruder括号内的值并转换为浮点数，赋值给extruder_value
                extruder_value = float(line.split('(')[1].split(')')[0])
            elif line.startswith('movej') or line.startswith('movel'):
                move_type = line.split('(')[0]
                # 提取movej或movel括号内的参数内容
                for i in line.split('[')[1].split(']')[0].split(','):
                    movepath.append(float(i))
                move_parameter_0 = line.split('],')[1].split(')')[0].split(',')[0]
                move_parameter_1 = line.split('],')[1].split(')')[0].split(',')[1]
                move_parameter_2 = line.split('],')[1].split(')')[0].split(',')[2]
                move_parameter_3 = line.split('],')[1].split(')')[0].split(',')[3]
                if len(movepath) == 6:
                    movement_dict[index] = [move_type, movepath, move_parameter_0, move_parameter_1, move_parameter_2, move_parameter_3, extruder_value]
                    movepath = []
                index += 1
                extruder_value = 0
            elif line.startswith('speed_ms'):
                continue
    return movement_dict

def print_position():
    global signal
    global now_position
    while signal:
        now_position = rtde_r.getActualTCPPose()
        print(rtde_r.getTargetTCPPose())
        time.sleep(0.05)  # 模拟耗时操作


if __name__ == "__main__":
    movement_sites = split_script('script.txt')

    speed_ = None
    accel_ = None
    options = None

    rtde_c = rtde_control.RTDEControlInterface(ROBOT_IP)
    rtde_r = rtde_receive.RTDEReceiveInterface(ROBOT_IP)

    thread = Thread(target=print_position)
    thread.daemon = True
    thread.start()


    path = rtde_control.Path()

    if rtde_c.isConnected():
        print("机械臂已经连接！")

        for key, value in movement_sites.items():
            # print(key, value)
            pose = value[1]  # 当前位姿 [x, y, z, rx, ry, rz]

            pose.append(speed_ms)
            pose.append(accel_mss)

            if value[4] == 'blend_radius_m':
                pose.append(blend_radius_m)
            else:
                pose.append(blend_radius_m)

            entry = rtde_control.PathEntry(rtde_control.PathEntry.MoveL, rtde_control.PathEntry.PositionTcpPose, pose)
            path.addEntry(entry)

    #   rtde_c.moveL(pose,speed_ms,accel_mss, asynchronous=True)
        rtde_c.moveL([0.009757, -0.460243, 0.121700, -0.000000, 3.141593, -0.000000], speed_ms, accel_mss)

        rtde_c.movePath(path, asynchronous=True)



        Data = 0
        while signal:
            data = rtde_c.getAsyncOperationProgress()
            if Data != data:
                # extruder("G1 E10 F300")
                print(data)
                Data = data
            if data < 0:
                signal = False
                thread.join()

    time.sleep(1)
    new_position = now_position
    new_position[2] = new_position[2] + 0.05
    rtde_c.moveL(new_position, speed_ms, accel_mss)