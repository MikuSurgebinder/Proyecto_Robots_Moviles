import rospy
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry


def split_input(input_str):
    # Split the input string by comma
    parts = input_str.split(',')

    # Check if there are exactly two parts
    if len(parts) == 2:
        return parts[0].strip(), parts[1].strip()
    else:
        raise ValueError("Input string must contain exactly one comma")
    
def get_pose_callback(data,pose):
    pose=data.pose
    return pose

def get_localization():
    pose=[]
    sub_location = rospy.Subscriber("/odom", Odometry, lambda data: get_pose_callback(data,pose))
    rospy.sleep(0.01)
    sub_location.unregister()
    return pose
