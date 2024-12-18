output = "```URscript\ndef pick_and_place():\n  local pick_pos = p[0.2, -0.3, 0.1, 0, 0, 0]\n  local place_pos = p[0.4, 0.3, 0.1, 0, 0, 0]\n  local home_pos = p[0,0,0.5,0,0,0]\n    \n  movej(get_inverse_kin(pick_pos, qnear=get_actual_joint_positions()), a=1.0, v=0.5)\n  set_digital_out(0, True)\n  sync()\n  sleep(0.5)\n  movej(get_inverse_kin(place_pos, qnear=get_actual_joint_positions()), a=1.0, v=0.5)\n  set_digital_out(0, False)\n  sync()\n  sleep(0.5)\n  movej(get_inverse_kin(home_pos, qnear=get_actual_joint_positions()), a=1.0, v=0.5)\nend\n```"

print(output)
