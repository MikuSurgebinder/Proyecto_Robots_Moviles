#Proyecto - Robots moviles

#Este módulo implementa la interfaz. De momento muestra los 3 botones compartidos con los reales (B0,B1,B2) y los tres extra digitales (D3,D4,D5)
#D3 -> 
#B4 -> Si los mantienes pulsados 2 segundos, sobreescriben la pose. (implementado en máquina de estados)
#B5 -> 

#Añadimos 3 botones extra por digital mediante la interfaz de python.
#Básicamente al clicar un boton se publica en su topic como "pressed" para luego con la maq estados para ver si >2seg


import roslib
import rospy
from kobuki_msgs.msg import ButtonEvent
from prm_buttons import ButtonEventCallback

class interface():
    def __init__(self):
        rospy.init_node("interface")		
        
		
    def digi_buttons():
        rospy.Subscriber("/mobile_base/events/button",ButtonEvent,self.ButtonEventCallback)
		

  
    
if __name__ == '__main__':
	try:
		real_buttons()
	except rospy.ROSInterruptException:
		rospy.loginfo("exception")