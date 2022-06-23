# This callback is associated with the move_xy state node.

# capture pose part of the odometry message to a shared variable
gd.shared.odom_position = msg.pose.pose.position
