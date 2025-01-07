import rtde_receive

rtde_r = rtde_receive.RTDEReceiveInterface("192.168.56.101")
actual_q = rtde_r.getActualQ()


def test_last_position():
    assert actual_q == [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
