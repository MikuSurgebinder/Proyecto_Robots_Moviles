import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

#Solo para testear
waypoint = [(5, 4), (0.0, 0.0, 0.0, 1.0)] #Coordenadas de ejemplo


 #Funcion para crear un punto (con coordenadas pasadas por variable) y ejecutar navegación hasta ese punto
def Moverse(w):
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction) #Ejecutar la accion de nav. para luego recibir coordenadas
    client.wait_for_server()

    goal_pose = MoveBaseGoal()  #Formatear la varible pasada a coordenadas para navegación
    goal_pose.target_pose.header.frame_id = 'map'
    goal_pose.target_pose.pose.position.x = w[0][0]
    goal_pose.target_pose.pose.position.y = w[0][1]
    goal_pose.target_pose.pose.position.z = 0.0
    goal_pose.target_pose.pose.orientation.x = w[1][0]
    goal_pose.target_pose.pose.orientation.y = w[1][1]
    goal_pose.target_pose.pose.orientation.z = w[1][2]
    goal_pose.target_pose.pose.orientation.w = w[1][3]
        
    client.send_goal_and_wait(goal_pose) #Envia petición y espera para que la maquina no termine prematuramente
    print("Fin del programa") #Como es la ultima accion antes de terminar la maquina, esta para debuggear y ver que vaya bien



if __name__ == '__main__': #Para testeo
    rospy.init_node('patrol')
    Moverse(waypoint)