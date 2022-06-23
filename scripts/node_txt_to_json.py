import sys
import json
import getpass
from datetime import datetime

parameters={}
ports={}

def parse_paramcomment(line):
	if (len(line)==0):
		return '' #empty line
		
	comment =  line.strip();#remove spaces
	# print(list(ports.keys()))#get the last port added
	
	# print(f'good comment <{comment}>')
	last_added_param = list(parameters.keys())[-1]
		# print( last_added_port )
	parameters[last_added_param]["Description"]=comment

def parse_params(line):
    # print(line)
	#if there is no default, it is a commnent
    if (-1 == line.find('default')):
        parse_paramcomment(line)
    else:
        s1=line.find('(')
        param_name = line[0:s1-1]
        line = line[s1:]
        s2=line.find(',')
        param_type = line[1:s2] 
        line=line[s2:]
        s3=line.find('default:')
        default = line[s3+9:-1]
        print(f'={param_name}={param_type}={default}=')
        parameters[param_name]={}
        parameters[param_name]["Description"]=""
        parameters[param_name]["Value"]= default
	
	

def parse_portcomment(line):
	if (len(line)==0):
		return '' #empty line
		
	comment =  line.strip();#remove spaces
	# print(list(ports.keys()))#get the last port added
	
	# print(f'good comment <{comment}>')
	last_added_port = list(ports.keys())[-1]
		# print( last_added_port )
	ports[last_added_port]["Info"]=comment

def add_port(port_name,pkg_name,msg_name):
    if mode == 'in':
        ports[port_name]["Template"]="ROS1/Subscriber"
        ports[port_name]["In"]={}
        ports[port_name]["In"]["in"]={}
        ports[port_name]["In"]["in"]["Message"]=pkg_name+"/"+msg_name
    elif mode == 'out':
        ports[port_name]["Template"]="ROS1/Publisher"
        ports[port_name]["Out"]={}
        ports[port_name]["Out"]["out"]={}
        ports[port_name]["Out"]["out"]["Message"]=pkg_name+"/"+msg_name
    elif mode == 'service':
        ports[port_name]["Template"]="ROS1/ServiceServer"
        ports[port_name]["In"]={}
        ports[port_name]["In"]["in"]={}
        ports[port_name]["In"]["in"]["Message"]=pkg_name+"/"+msg_name
    elif mode == 'clientsrv':
        ports[port_name]["Template"]="ROS1/ClientServer"
        ports[port_name]["Out"]={}
        ports[port_name]["Out"]["out"]={}
        ports[port_name]["Out"]["out"]["Message"]=pkg_name+"/"+msg_name
	
    
def parse_ioport(line):
	# print(f'=<{line}>=, lenght = {len(line)}')
	#if you can find a <space( and a / then it is a Port
    if (-1 != line.find(' (') and -1 != line.find('/')):
    # print('Found ( and /.')
    #expected style--> param_name (type, default: defvalue)')
        s1=line.find('(')
        port_name = line[0:s1-1]
        line = line[s1:]
        s2=line.find('/')
        pkg_name = line[1:s2]
        line = line[s2+1:]
        msg_name = line[0:-1]
        # print(f'={port_name}={pkg_name}={msg_name}=')
        ports[port_name]={}
        ports[port_name]["Package"]=pkg_name
        ports[port_name]["Message"]=msg_name
        ports[port_name]["Info"]=""
        print(f'identified: ={port_name}={pkg_name}={msg_name}=')
        add_port(port_name,pkg_name,msg_name)
    else:
        # print('no port description. so comment or empty space?')
        parse_portcomment(line)


           
 # parses all lines that are NOT "Titles".
def parser(line, mode):
	if mode == 'in' or mode == 'out' or mode == 'service'  or mode == 'clientsrv':
		parse_ioport(line)
	elif mode == 'param':
		parse_params(line)
	else :
		print(f'unknown mode {mode}')

# code starts here 

print("Filename to read: ",sys.argv[1])
		               
idict ={}
filename = sys.argv[1] # filename = 'aloam_manifest.txt'

# read the whole file into <lines>
with open(filename,'r') as f:
	lines = f.readlines()


mode = -1 #-1 invalid. keeps track of which Section from the text we currently are

# keep reading lines 
for idx in range(0,len(lines)):
	line=lines[idx]
	line=line[0:-1]#remove the \n
	
    #these are the accepted Sections/Titles names
	if line == 'Subscribed Topics' :
		print("listing Subcribers.")
		mode= 'in'
	elif line == 'Published Topics':
		print("listing Publishers.")
		mode= 'out'
	elif line == 'Services':
		print("listing ServerServices.")
		mode= 'service'
	elif line == 'Services Called':
		print("listing ClientServices.")
		mode= 'clientsrv'
	elif line == 'Parameters':
		print("listin Parameters.")
		mode= 'param'
	else:
		# pparses the content of each section 
		parser(line,mode)
		

print("Parsing is Done")


nodename =filename[0:-13]# nodename is infered from the prefix before "_manifest.txt" (13 chars)

# build a dictionary
idata={}
idata["Node"]={};
idata["Node"][nodename]={}
idata["Node"][nodename]["Label"]= nodename
idata["Node"][nodename]["Launch"]=True
idata["Node"][nodename]["Persistent"] =True
idata["Node"][nodename]["Type"]= "ROS1/Node"
idata["Node"][nodename]["Parameter"]= parameters
idata["Node"][nodename]["PortsInst"]= ports
idata["Node"][nodename]["LastUpdate"]={}
idata["Node"][nodename]["LastUpdate"]["date"] = datetime.now().strftime("%d/%m/%Y at %H:%M:%S")
# date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
idata["Node"][nodename]["LastUpdate"]["user"] = getpass.getuser()
idata["Node"][nodename]["Path"]= "/../../../mov.ai/workspaces/USER_ROS1/lib/<please_complete_this>"

#dump dictionary to a json file.
with open(f'database/precious_work/Node/{nodename}.json', "w") as write_file:
    json.dump(idata, write_file)


print(f'File {nodename}.json has been written')
