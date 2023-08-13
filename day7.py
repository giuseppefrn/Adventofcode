import os
import re

#logger section
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("Log")
logger.setLevel(logging.DEBUG)
os.makedirs("logs", exist_ok=True)
handler = RotatingFileHandler("logs/day7.log", maxBytes=100000, backupCount=5)
logger.addHandler(handler)

current_path = [] #used to track current dir

subdirs = {} 
dir_sizes = {}

total_disk_space = 70000000
total_required_disk_space = 30000000
dir_total_sizes = {}

def parse_inputs(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    sizes = [] 
    abs_path = '/'

    for line in lines:
        line = re.sub('\n', '', line)
        logger.debug(f"line: {line}")
        if line.startswith("$ "): #it is a command
            command = line.split(" ")
            instruction = command[1]

            logger.debug(instruction)

            if instruction == "cd":
                if len(sizes) > 0 or abs_path not in dir_sizes.keys():
                    #before changing dir update current dir size
                    dir_size = sum(sizes)
                    dir_sizes[abs_path] = dir_size
                    sizes = [] #reset sizes
                    logger.debug(f"dir_sizes: {dir_sizes}")

                argument = command[2]
                logger.debug(argument)
                
                if argument == "..": 
                    logger.debug("moving back")
                    current_path.pop() #move back from current dir
                else:
                    logger.debug("moving forward")
                    current_path.append(argument) #navigate to the next dir

                #update abs_path
                abs_path = os.path.join(*current_path) #current dir absolute path
                logger.debug(f"current path: {current_path}")
                logger.debug(f"update abs_path: {abs_path}")
                    
        else: #it is ls outputs
            command_output = line.split(" ")
            if command_output[0] == "dir":
                #save subdir to parent's list
                logger.debug(command_output)
                dir_name = command_output[1]

                subdir_name = os.path.join(abs_path,dir_name)
                
                if abs_path not in subdirs.keys(): #the list doesn't exist
                    subdirs[abs_path] = []

                subdirs[abs_path].append(subdir_name) #add path to subfolders list of the current dir
                logger.debug(f"subdirs: {subdirs}")

            else: #it is a file size
                #update the size
                sizes.append(int(command_output[0]))
                logger.debug(int(command_output[0]))
    #last update 
    dir_size = sum(sizes)
    dir_sizes[abs_path] = dir_size
    sizes = [] #reset sizes
    logger.debug(f"dir_sizes: {dir_sizes}")

def calculate_total_size(abs_path):
    size = dir_sizes[abs_path]

    if abs_path in subdirs.keys():
        for subdir in subdirs[abs_path]:
            size += calculate_total_size(subdir)

    logger.debug(f"total size {abs_path} : {size}")
    return size


if __name__ == "__main__":
    parse_inputs("./pazzle_inputs.in")

    ans = 0
    for dir in dir_sizes.keys():
        logger.debug(f"dir: {dir}")
        total_size = calculate_total_size(dir)
        dir_total_sizes[dir] = total_size
        if total_size <= 100000:
            ans += total_size
    
    logger.debug(f"subdirs: {subdirs}")
    logger.debug(f"dir_sizes: {dir_sizes}")

    print(f"part 1 completed: {ans}")


    free_space = total_disk_space - dir_total_sizes['/'] 
    required_dick_space = total_required_disk_space - free_space

    ans_2 = 2**64
    for v in dir_total_sizes.values():
        if v >= required_dick_space and v < ans_2:
            ans_2 = v

    print(f"part 2 completed: {ans_2}")