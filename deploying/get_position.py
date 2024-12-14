from rtde_receive import RTDEReceiveInterface
import time

robot_ip = "192.168.1.100"

try:
    # Create RTDE receiver object
    rtde_r = RTDEReceiveInterface(robot_ip)

    while True:
        # Get the TCP position
        tcp_pose = rtde_r.getActualTCPPose()

        # Get the joint positions
        joint_positions = rtde_r.getActualQ()

        # Print the TCP pose and joint positions
        print(f"Tool Pose (TCP): {tcp_pose}")  # [X, Y, Z, Rx, Ry, Rz]
        print(f"Joint Positions: {joint_positions}")  # [Base, Shoulder, Elbow, Wrist1, Wrist2, Wrist3]

        # Wait before the next iteration
        time.sleep(1)  # Adjust frequency as needed

except Exception as e:
    print(f"An error occurred: {e}")
