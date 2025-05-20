import time

import rtde_receive

if __name__ == '__main__':
    rtde_r = rtde_receive.RTDEReceiveInterface("192.168.106.128")
    while  True:
        tcp_speed = rtde_r.getActualTCPSpeed()
        tcp_position = rtde_r.getActualTCPPose()
        time.sleep(0.25)
        print([round(x, 3) for x in tcp_position])
        print([round(x, 3) for x in tcp_speed])