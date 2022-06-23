#logger.info('NEW MESSGE ODOMETRY')

#logger.info(f'new msg: {msg.mypose.mypose.position.x},{msg.mypose.mypose.position.y}')


if gd.shared.mypath is None:
    logger.info("creating empty Path object")
    mypath = Path()
    logger.info("just created a empty Path object")
else:
    mypath = gd.shared.mypath #load existing path


#To avoid repeating the values, check if received values are different:
dist = (gd.shared.odo_x - float(msg.pose.pose.position.x))**2 + \
(gd.shared.odo_y - float(msg.pose.pose.position.y))**2 + \
(gd.shared.odo_z - float(msg.pose.pose.position.z))**2
if dist > 0.5:

    # new Pose to add:
    # create a copy of odometry msg to  type myposestamped
    mypose = PoseStamped()    
    mypose.pose = msg.pose.pose
    mypose.header = msg.header
  
    if 0:
        mypose.pose.position.x = float(msg.pose.pose.position.x)
        mypose.pose.position.y = float(msg.pose.pose.position.y)
        mypose.pose.position.z = float(msg.pose.pose.position.z)
        mypose.pose.orientation.x = float(msg.pose.pose.orientation.x)
        mypose.pose.orientation.y = float(msg.pose.pose.orientation.y)
        mypose.pose.orientation.z = float(msg.pose.pose.orientation.z)
        mypose.pose.orientation.w = float(msg.pose.pose.orientation.w)
        mypose.child_frame_id = msg.child_frame_id
    
    
    
    #Set a atributes of the Path
    mypath.header.seq = gd.shared.counter
    mypath.header.stamp = rospy.Time.now()
    mypath.header.frame_id = "worldframe"
       
    # time to add this mypose to the list 
    mypath.poses.append(mypose)
    #Published the msg

    gd.shared.counter = gd.shared.counter+1
    gd.shared.mypath = mypath 

    gd.shared.odo_x = msg.pose.pose.position.x
    gd.shared.odo_y = msg.pose.pose.position.y
    gd.shared.odo_z = msg.pose.pose.position.z

gd.oport['path_out'].send(mypath)