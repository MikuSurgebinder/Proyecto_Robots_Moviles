#Estudiante: Gumiel Rico, Gemma
#Practica 3 - Robots moviles

import rospy
from smach import StateMachine
from smach_ros import SimpleActionState
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

#Esta funcion indica a que punto regresar: el origen establecido en (5,4)
#Aqui surge un problema, que no influye en el funcionamiento del programa, pero 
#que deja colgada la terminal tras acabar de volver a la pose indicada...

def volver():
    #rospy.init_node('patrol')#no 
    waypoints = [
        ['Casa', (5,4), (0.0, 0.0, 0.0, 1.0)]]
    patrol = StateMachine(['succeeded','aborted','preempted'])
    with patrol:
        for i,w in enumerate(waypoints):
            goal_pose = MoveBaseGoal()
            goal_pose.target_pose.header.frame_id = 'map'
            goal_pose.target_pose.pose.position.x = w[1][0]
            goal_pose.target_pose.pose.position.y = w[1][1]
            goal_pose.target_pose.pose.position.z = 0.0
            goal_pose.target_pose.pose.orientation.x = w[2][0]
            goal_pose.target_pose.pose.orientation.y = w[2][1]
            goal_pose.target_pose.pose.orientation.z = w[2][2]
            goal_pose.target_pose.pose.orientation.w = w[2][3]
            StateMachine.add(w[0],SimpleActionState('move_base', MoveBaseAction, goal=goal_pose),transitions={'succeeded':waypoints[(i + 1) % len(waypoints)][0]})
    patrol.execute()
