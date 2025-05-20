import time

import rtde_control
import rtde_receive


def demo1():
    rtde_c = rtde_control.RTDEControlInterface("192.168.106.128")
    rtde_c.moveL([-0.5, -0.1, 0.350, -0.0, 3.141593, -0.0], 0.5,2.0)
    # time.sleep(0.5)
    # rtde_c.moveL([-0.7, -0.3, 0.15, -0.0, 3.141593, -0.0], 0.5,2.0)
    # time.sleep(0.5)
    # rtde_c.moveL([-0.5, -0.1, 0.15, -0.0, 3.141593, -0.0], 0.5, 2.0)
    # time.sleep(0.5)
    # rtde_c.moveL([-0.7, -0.3, 0.15, -0.0, 3.141593, -0.0], 0.5, 2.0)
    # time.sleep(0.5)
    # rtde_c.moveL([-0.5, -0.1, 0.15, -0.0, 3.141593, -0.0], 0.5, 2.0)
    # time.sleep(0.5)
    # rtde_c.moveL([-0.7, -0.3, 0.15, -0.0, 3.141593, -0.0], 0.5, 2.0)
    # time.sleep(0.5)
    # rtde_c.moveL([-0.5, -0.1, 0.15, -0.0, 3.141593, -0.0], 0.5, 2.0)
    # time.sleep(0.5)
    # rtde_c.moveL([-0.7, -0.3, 0.15, -0.0, 3.141593, -0.0], 0.5, 2.0)
    # rtde_c.speedL(xd=[0.05, 0.0, 0.0, 0.0, 0.0, 0.0], acceleration=.5, time=2.0)
    # time.sleep(1)
    # rtde_c.speedL(xd=[0.0, 0.05, 0.0, 0.0, 0.0, 0.0], acceleration=.5, time=2.0)
    # time.sleep(1)
    # rtde_c.stopL()
    rtde_c.disconnect()

def  demo2():
    # 初始化 RTDEControlInterface
    robot_ip = "192.168.106.128"
    rtde_c = rtde_control.RTDEControlInterface(robot_ip)
    rtde_r = rtde_receive.RTDEReceiveInterface(robot_ip)
    print(rtde_r.getActualTCPPose())

    try:
        # 第一阶段：X 方向匀速移动 2 秒
        print("开始 X 方向移动...")
        rtde_c.speedL(xd=[0.05, 0.0, 0.0, 0.0, 0.0, 0.0], acceleration=0.5, time=2.0)
        time.sleep(2.5)  # 等待足够时间让指令执行完毕（2秒 + 安全余量）
        print(rtde_r.getActualTCPPose())
        # 第二阶段：Y 方向匀速移动 2 秒
        print("开始 Y 方向移动...")
        rtde_c.speedL(xd=[0.0, 0.05, 0.0, 0.0, 0.0, 0.0], acceleration=0.5, time=2.0)
        time.sleep(2.5)  # 等待执行完毕
        print(rtde_r.getActualTCPPose())
        # 停止运动
        print("停止运动")
        rtde_c.stopL()
        time.sleep(0.5)
        print(rtde_r.getActualTCPPose())

    finally:
        # 断开连接
        rtde_c.disconnect()
        print("已断开与机器人的连接")

if __name__ == '__main__':
    demo1()
    time.sleep(2)
    demo2()

