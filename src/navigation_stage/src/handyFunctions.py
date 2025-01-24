<<<<<<< HEAD
import rospy
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
=======
# Librerías a usar
import rospy, cv2, cv_bridge
import numpy as np
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import Image
from geometry_msgs.msg import Pose
from nav_msgs.msg import Odometry
pose = Pose()
>>>>>>> 91f3c6f3439f0cbca12fdd03051b3b1277066f36


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

#Suscribir al topic del robot una vez, pillarlo, ponerlo en pose y desub
def get_localization():
<<<<<<< HEAD
    pose=[]
    sub_location = rospy.Subscriber("/odom", Odometry, lambda data: get_pose_callback(data,pose))
    rospy.sleep(0.01)
    sub_location.unregister()
=======
    global pose
    def callback_get_loc(msg):
        global pose
        pose = msg.pose.pose
        #print(pose)
        odom_sub.unregister()
    odom_sub = rospy.Subscriber('/odom', Odometry, callback_get_loc) #Robot simulado
    rospy.sleep(0.0001)
>>>>>>> 91f3c6f3439f0cbca12fdd03051b3b1277066f36
    return pose

def moverse(w):
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction) #Ejecutar la accion de nav. para luego recibir coordenadas
    client.wait_for_server()

    goal_pose = MoveBaseGoal()  #Formatear la varible pasada a coordenadas para navegación
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.pose.position.x = w.position.x
    goal_pose.target_pose.pose.position.y = w.position.y
    goal_pose.target_pose.pose.position.z = w.position.z
    goal_pose.target_pose.pose.orientation.x = w.orientation.x
    goal_pose.target_pose.pose.orientation.y = w.orientation.y
    goal_pose.target_pose.pose.orientation.z = w.orientation.z
    goal_pose.target_pose.pose.orientation.w = w.orientation.w
        
    client.send_goal_and_wait(goal_pose) #Envia petición y espera para que la maquina no termine prematuramente
    print("Fin del programa") #Como es la ultima accion antes de terminar la maquina, esta para debuggear y ver que vaya bien

    

if __name__ == '__main__':
    rospy.init_node("handyFunctionsDebugg")
    
    
    #Debugg get pose
    pose = get_localization()
    print(pose)
    
    
    
    #rospy.spin()