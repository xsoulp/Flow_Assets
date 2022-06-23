
logger.info('ENTER TARGET GEN')


file = open("/opt/mov.ai/user/" + gd.params["file_name"], "r")


array_x = []
array_y = []
array_z = []
array_times = []

# ler ficheiro de caminho
logger.info("starting the file")
line = file.readline()
while (line != ""): 
    linetup = line.split()
    (c_x, c_y, c_t) = linetup
    array_x.append(float(c_x))
    array_y.append(float(c_y))
    array_z.append(float(3))
    array_times.append(float(c_t))
    logger.info("reading ...")
    line = file.readline()


# save globals
gd.shared.target_array_x = array_x 
gd.shared.target_array_y = array_y
gd.shared.target_array_z = array_z
gd.shared.timestamps = array_times
now = rospy.get_rostime()
gd.shared.init_simclock = now.secs
gd.shared.target_idx = 0

file.close()
