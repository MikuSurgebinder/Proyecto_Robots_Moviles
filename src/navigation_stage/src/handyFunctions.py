from geometry_msgs.msg import Pose

def split_input(input_str):
    # Split the input string by comma
    parts = input_str.split(',')

    # Check if there are exactly two parts
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    else:
        raise ValueError("Input string must contain exactly one comma")
    

def get_localization():
    pose = Pose()
    #Suscribir al topic del robot, pillarlo, ponerlo en pose y desub

    return pose
