
timestamps  = gd.shared.timestamps
arr_x = gd.shared.target_array_x
arr_y = gd.shared.target_array_y
arr_z = gd.shared.target_array_z
idx = gd.shared.target_idx
    
odom_position = gd.shared.odom_position

mymsg = Point()
mymsg.x = arr_x[idx]
mymsg.y = arr_y[idx]
mymsg.z = arr_z[idx]
gd.oport["targets"].send(mymsg)
time = rospy.Time.now()

now = rospy.get_rostime()
current_distance = sqrt( (mymsg.x - odom_position.x)**2 + (mymsg.y - odom_position.y)**2 + (mymsg.z - odom_position.z)**2 )
if (current_distance < 0.2):
    logger.info("Target reached")

    if (now.secs > timestamps[idx] + gd.shared.init_simclock + 3):
        logger.info("timer reached!")
        gd.shared.target_idx = gd.shared.target_idx + 1
        logger.info(f'Target: {gd.shared.target_idx}/{len(arr_x)}')
        if (gd.shared.target_idx >= len(arr_x)): 
            logger.info('TIME TO FINISH')
            mymsg.z = -1
            gd.oport["targets"].send(mymsg)
            rospy.sleep(0.1)
            gd.oport["exit"].send()
