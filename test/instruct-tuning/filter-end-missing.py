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

no_end_code = """
```URscript
def adjust_z_based_on_sensor(sensor_threshold):
  sensor_data = 60  # Assume sensor input - Replace with actual sensor read
  current_pose = get_actual_tcp_pose()
  
  if sensor_data > sensor_threshold:
    new_z = current_pose[2] + 0.05
    if new_z <= 0.5:  # Check motion limit
      target_pose = p[current_pose[0],current_pose[1], new_z, current_pose[3], current_pose[4], current_pose[5]]
      movel(target_pose, a=0.3,v=0.2)
    else:
      textmsg(""Warning: Z-axis limit reached up."")
  else:
     new_z = current_pose[2] - 0.05
     if new_z >= 0.1: # Check motion limit
       target_pose = p[current_pose[0],current_pose[1], new_z, current_pose[3], current_pose[4], current_pose[5]]
       movel(target_pose, a=0.3,v=0.2)
     else:
      textmsg(""Warning: Z-axis limit reached down."")
end
adjust_z_based_on_sensor(50)
```
"""


# TODO: add regex later
def detect_missing_end(incomplete_code: str) -> bool:
    """
    Check if the given URScript code has missing 'end' keywords.

    :param incomplete_code: The incomplete URScript code as a string.
    :return: False if any 'def' is missing its corresponding 'end', True otherwise.
    """
    # Count the occurrences of 'def' and 'end'
    keywords = ["def ", "while ", "if ", "thread "]
    keywords_count = sum(incomplete_code.count(keyword) for keyword in keywords)

    end_count = incomplete_code.count("end")
    print(keywords_count)
    print(end_count)

    # Return False if 'end' count is less than 'def' count
    return keywords_count == end_count


# Example usage
incomplete_code_1 = """
def move_to_given_joint_and_log():
    global target_joint_pos
    log_message = "Starting joint positions "
    joint_positions = get_actual_joint_positions()
"""

# Test the function
print("Valid code: ", detect_missing_end(valid_code))  # Expected: False
print("Missing 'end':", detect_missing_end(incomplete_code_1))  # Expected: True
