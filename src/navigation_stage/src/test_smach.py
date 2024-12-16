from __future__ import print_function

import rospy
import smach_ros
import math
from smach import State,StateMachine
from time import sleep
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

posicion=[6]


class Quieto(State):
    def __init__(self):
        State.__init__(self, outcomes=['buttonPressed','followPerson'])
    
    def execute(self, userdata):
        #Velocidad=0 y pub
        while True:
            if 'echo en callback de boton'==True: 
                return 'buttonPressed'
            if 'echo en callback de seguimiento'==True:
                return 'followPerson'
            
class Boton(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        #Detectar que boton se ha pulsado y como
        boton = Boton() #Crear clase boton con métodos e importarlo
        while True:
            if 'boton . tipo de presionado() '== 'largo':
                posicion[boton.numBoton()] = getLocalizacion() #Crear handyFunciones e importarlo
                break
            if 'boton . tipo de presionado() '== 'corto':
                irLocalizacion(posicion[boton.numBoton()])
                esperarATerminar()
                break
        return 'success'



class Seguimiento(State): #Segundo estado de la maquina
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        bandera = True
        while bandera:
            dir = vision() #Importar de Erika
            seguimiento(dir) #Importar de Gemma
            if CambioDeOrden:
                return 'success'




if __name__ == '__main__':
    rospy.init_node("test_smach")

    #Maquina de estados
    sm = StateMachine(outcomes=['stop'])
    with sm:
        StateMachine.add('WaitingForOrders', Quieto(), transitions={'buttonPressed':'ButtonCommand','followPerson':'FollowCommand'})
        StateMachine.add('ButtonCommand', Boton(), transitions={'success':'WaitingForOrders'})
        StateMachine.add('FollowCommand', Seguimiento(), transitions={'success':'WaitingForOrders'})
    
    #"sis" solo sirve para mostrar una representación gráfica de la máquina de estados    
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    sm.execute()
    rospy.spin()
    sis.stop()
