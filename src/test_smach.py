from __future__ import print_function

import rospy
import smach_ros
import math
from smach import State,StateMachine
from time import sleep
from practica3_base import WanderAndDetect
from volver_origen import Moverse

"""
#Topics a usar en suscripciones y publicaciones
TOPIC_VEL = "/cmd_vel"
TOPIC_SCAN = '/base_scan'
TOPIC_COLOR = '/color_detected'

#Nos fijamos en el ángulo a 30 y -30 grados, podéis cambiarlo si quereis.
#Se ha añadido más adelante utilizar el haz frontal.
ANG_IZQ = 30*math.pi/180.0
ANG_DER = -ANG_IZQ
"""

"""
class Uno(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        print('Deambular hasta encontrar rojo')
        color_detected = False
        a = WanderAndDetect()
        while not color_detected:
            color_detected = not a==""
        sleep(1)
        print('Rojo encontrado')
        return 'success'
"""

class Dos(State): #Segundo estado de la maquina
    def __init__(self):
        State.__init__(self, outcomes=['end'])
    
    def execute(self, userdata):
        print('Volver a casa')
        Moverse(([5,4],[0,0,0,1])) #Volver a casa, coordenadas especificadas a mano, código en volver_origen.py
        sleep(1)
        return 'end' #Finaliza la maquina de estados



if __name__ == '__main__':
    rospy.init_node("test_smach")

    #Maquina de estados
    sm = StateMachine(outcomes=['stop'])
    with sm:
        StateMachine.add('WanderUntilRed', WanderAndDetect(), transitions={'success':'ACasita'}) #Deambular hasta encontar rojo, en practica3_base.py
        StateMachine.add('ACasita', Dos(), transitions={'end':'stop'}) #Navegación de volver al origen
    
    #"sis" solo sirve para mostrar una representación gráfica de la máquina de estados    
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    sm.execute()
    rospy.spin()
    sis.stop()
