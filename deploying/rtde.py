import rtde_receive

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.56.101")
actual_q = rtde_r.getTargetTCPSpeed()
print(actual_q)
