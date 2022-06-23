
# parameters
#target_x = float(gd.params['target_x'])
target_x = gd.shared.target_array_x
target_y = gd.shared.target_array_y
target_z = gd.shared.target_array_z
max_vel = float(gd.params['max_vel'])
distance_error = float(gd.params['distance_error'])
kp = 0.8*float(gd.params['kp'])

def looper():
    
    # get odometry messages
    odom_position = gd.shared.odom_position
    if odom_position is None:
        logger.info('No odom yet')
        return

    #get target
    if gd.shared.mylastarget is None:
        logger.info('No TARGET yet')
        return

    target_pt = gd.shared.mylastarget
    target_x = target_pt.x
    target_y = target_pt.y
    target_z = target_pt.z
    
    # get current distance

    logger.info(f'target: {target_x},{target_y}')
    vel = Twist()
    vel.linear.x = kp*(target_x - odom_position.x)
    vel.linear.x = min(max_vel, max(-max_vel, vel.linear.x))

    vel.linear.y = kp*(target_y - odom_position.y)
    vel.linear.y = min(max_vel, max(-max_vel, vel.linear.y))
    
    vel.linear.z = kp*(target_z - odom_position.z)
    gd.oport['cmd_vel'].send(vel)

        



looper()