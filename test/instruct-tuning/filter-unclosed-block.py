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


# try with `missing code` output first
def detect_unclosed_urscript_blocks(code: str) -> bool:
    """
    Detect whether all ` ```URscript ` blocks in the code have corresponding closing ` ``` `.

    :param code: The input code as a string.
    :return: True if all blocks are properly closed, False otherwise.
    """
    lines = code.splitlines()
    open_blocks = 0

    for line in lines:
        # Detect opening block
        if line.strip() == "```URscript" or line.strip() == "```urscript":
            open_blocks += 1
        # Detect closing block
        elif line.strip() == "```":
            if open_blocks > 0:
                open_blocks -= 1

    # If open_blocks is 0, all blocks are properly closed
    return open_blocks == 0


# Example inputs
missing_code = """
```urscript
def debug_issue():
  local target_pose = p[0.4, -0.3, 0.5, 0, 0, 0]
  movej
"""

unclosed_block = detect_unclosed_urscript_blocks(missing_code)
print(f"detect unclosed block: {unclosed_block}")

closed_block = detect_unclosed_urscript_blocks(valid_code)
print(f"detect closed block: {closed_block}")
