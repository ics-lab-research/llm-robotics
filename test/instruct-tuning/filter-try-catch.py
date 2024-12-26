valid_code = """
```URscript
def pick_and_place():
    local pick_pose = p[0.2, -0.4, 0.1, 0, 0, 0]
    local place_pose = p[0.4, -0.2, 0.1, 0, 0, 0]
    local approach_z = 0.2

    # Approach pick position
    movel(pose_add(pick_pose,p[0,0,approach_z,0,0,0]),a=1.0,v=0.5)

    # Move to pick position
    movel(pick_pose,a=0.5,v=0.2)

    # Close the gripper
    gripper_close()
    sleep(1)

    # Move to approach pose before lift
    movel(pose_add(pick_pose,p[0,0,approach_z,0,0,0]),a=0.5,v=0.4)

    # Move to the place position approach
    movel(pose_add(place_pose,p[0,0,approach_z,0,0,0]),a=1.0,v=0.5)

    # Move to place position
    movel(place_pose,a=0.5,v=0.2)

    # Open the gripper
    gripper_open()
    sleep(1)

    # Move to approach pose before going up
    movel(pose_add(place_pose,p[0,0,approach_z,0,0,0]),a=0.5,v=0.4)
end
```
"""


# TODO: avoid mistake try-catch keywork in comment
def detect_unavailable_keywords(
    code: str, keywords: list = ["try", "catch", "for"]
) -> bool:
    """
    Detect the presence of specified keywords in the code.

    :param code: The input code as a string.
    :param keywords: A list of keywords to detect.
    :return: False if any keyword is detected, True otherwise.
    """
    lines = code.splitlines()

    for line in lines:
        stripped_line = line.strip()
        for keyword in keywords:
            if stripped_line.startswith(keyword):
                return False

    return True


# Example inputs
try_catch_code = """
```URscript
def move_with_error_handling():
  safe_pos=p[0.0, 0.0, 0.2, 0.0, 0.0, 0.0]
  target_pos = p[0.2, 0.2,0.2,0.5,0.2,0.9]
  try:
    movej(target_pos, a=0.5, v=1)
  catch e:
    textmsg(""Movej failed, attempting recovery"", e)
    log_message(""Movej failed, attempting recovery."")
    movel(safe_pos, a=0.3, v=0.2)
  end
end
move_with_error_handling()
```
"""

for_code = """
```URscript
def move_through_waypoints(waypoints):
  blend_radius = 0.04 # Adjust this for smoother transitions
  q_prev = get_joint_positions()
  for q_next in waypoints:
    movej(q_next, a=0.5 ,v=1, r=blend_radius)
    q_prev = q_next
  end
end
```
"""

# Test the function
result1 = detect_unavailable_keywords(valid_code)
result2 = detect_unavailable_keywords(try_catch_code)
result3 = detect_unavailable_keywords(for_code)

# Print results
print("Valid code: ", result1)
print("Try-catch available: ", result2)
print("For available: ", result3)
