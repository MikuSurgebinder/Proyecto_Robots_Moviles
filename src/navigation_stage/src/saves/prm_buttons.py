#Proyecto - Robots moviles

#Este módulo es para la funcionalidad de los botones reales
#B0 -> 
#B1 -> Guardan la pose actual si los mantienes pulsados 2 segundos, sobreescribiendo las que estaban guardadas antes
#B2 -> 

#Añadimos 3 botones extra por digital mediante la interfaz de python.

import roslib
import rospy
from kobuki_msgs.msg import ButtonEvent

class real_buttons():
    def __init__(self):
        rospy.init_node("buttons")		
        #monitor kobuki's button events
        rospy.Subscriber("/mobile_base/events/button",ButtonEvent,self.ButtonEventCallback)
        #rospy.spin() tells the program to not exit until you press ctrl + c.  
        #If this wasn't there... it'd subscribe and then immediatly exit (therefore stop "listening" to the thread).
        rospy.spin()

    def ButtonEventCallback(self,data):
        if (data.state == ButtonEvent.RELEASED) :
            state = "released"
        else:
            state = "pressed" 
        #Botones reales (turtlebot2)
        if (data.button == ButtonEvent.Button0) :
            button = "B0"
        elif ( data.button == ButtonEvent.Button1) :
            button = "B1"
        elif (data.button == ButtonEvent.Button2):
            button = "B2"
        #rospy.loginfo("Button %s was %s."%(button, state))
        
        #ahora le guardariamos la pose para llamar a crear landmark   #~~~~~~~~~~~
        pose = odometry.now()
        real_buttons.landmark(pose, id)                                                          #~~~~~~~~~~~
    #Botones digitales (interfaz) ----------------------> Tengo que crear en el objeto 3 botones....
    #def DigitalButtonCallback(self,data):

if __name__ == "__main__":
    try:
        real_buttons()
    except rospy.ROSInterruptException:
        rospy.loginfo("exception")