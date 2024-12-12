#Estudiante: Gumiel Rico, Gemma
#Practica 3 - Robots moviles

from __future__ import print_function
import rospy
import smach_ros
from smach import State,StateMachine
from time import sleep
from practica3_base import WanderAndDetect
from color_detector import ColorDetector
from smach_actionstate import volver
#from sensor_msgs.msg import Image #para desuscribirse de la camara

class Navega(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        print('Navegando')
        gofre = WanderAndDetect()  #gofre es el robot
        #Navegamos hasta encontrar rojo, esta la camara activa tambien
        gofre.execute()
        self.color_detected = False 
        #self.subColor.unregister()
        #self.image_sub = rospy.Subscriber('/image', Image, self.image_callback)
        return 'success'

class Casa(State):
    def __init__(self):
        State.__init__(self, outcomes=['end'])
    
    def execute(self, userdata):
        print('Volviendo a origen: (5,4)')
        volver()
        return 'end'

if __name__ == '__main__':
    rospy.init_node("test_smach")
    sm = StateMachine(outcomes=['stop'])
    with sm:
        StateMachine.add('Navegando', Navega(), transitions={'success':'Casa'})
        StateMachine.add('Casa', Casa(), transitions={'end':'stop'})#para que termine, no está en bucle
    #"sis" solo sirve para mostrar una representación gráfica de la máquina de estados    
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    sm.execute()
    rospy.spin()
    sis.stop()
