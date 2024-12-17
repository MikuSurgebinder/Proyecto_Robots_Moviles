from __future__ import print_function

import rospy
import smach_ros
import math
from smach import State,StateMachine
from time import sleep
from volver_origen import Moverse
from vision import TurtleCamProcessor
from std_msgs.msg import String

from handyFunctions import split_input,get_localization

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

saved_buttons = {
    'B0': None, 'B1': None, 'B2': None,  # Physical buttons
    'D3': None, 'D4': None, 'D5': None,   # Digital buttons
    'WAIT': None
}




position=[] #Esturcura de posicion: es un vector con 6 posiciones almacenadas:
             #Cada posicion contiene una matriz, una fila con 3 coord de posicion (x,y,z)
             #y otra con 4 coord de orientacion (x,y,z,w)


class Static(State):
    def __init__(self):
        State.__init__(self, outcomes=['buttonPressed','followPerson','mapping'])
    
    def execute(self, userdata):
        #Velocidad=0 y pub

        print("Estado parado")
        while True:
            if saved_buttons['WAIT'] is not None:
                saved_buttons['WAIT']=None
                return 'followPerson'
            """
            if 'echo en callback de boton'==True: 
                return 'buttonPressed'
            if 'echo en callback de seguimiento'==True:
                return 'followPerson'
            if 'echo en callback de mapeado'==True:
                return 'mapping'
            """
class Button(State):
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        for i in range(len(saved_buttons)-1):
            if saved_buttons[i]== 'long':
                position[i] = get_localization() #Crear handyFunciones e importarlo
            if saved_buttons[i]== 'short':
                Moverse(position[i])
    
        return 'success'
        



class Follow(State): #Segundo estado de la maquina
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        bandera = False
        processor = TurtleCamProcessor()
        rospy.sleep(0.1)
        print("Estado camara seguimiento")
        try:
            rate = rospy.Rate(10)  # Procesa frames a 10 Hz
            while not rospy.is_shutdown():
                processor.process_frame()
                dir = [processor.area,processor.x_coord,processor.y_coord]
                print(dir)
                rate.sleep()
                if saved_buttons['WAIT'] is not None:
                    saved_buttons['WAIT']=None
                    bandera=True
        except bandera: #rospy.ROSInterruptException or 
            pass
        finally:
            processor.cleanup()
        return 'success'


class Map(State): #Segundo estado de la maquina
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        #Llamar a mapeado con deambulacion
            return 'success'





def callback_button(msg):
    button_name, button_state = split_input(msg.data)
    saved_buttons[button_name] = button_state 







if __name__ == '__main__':
    rospy.init_node("test_smach")

    #En el arranque, añadir un lector de datos para las localizaciones guardadas previamente

    #Callback de la interfaz y de los botones reales
    subColor = rospy.Subscriber("/button_communication", String , callback_button)


    #Maquina de estados
    sm = StateMachine(outcomes=['stop'])
    with sm:
        StateMachine.add('WaitingForOrders', Static(), transitions={'buttonPressed':'ButtonCommand','followPerson':'FollowCommand','mapping':'MapCommand'})
        StateMachine.add('ButtonCommand', Button(), transitions={'success':'WaitingForOrders'})
        StateMachine.add('FollowCommand', Follow(), transitions={'success':'WaitingForOrders'})
        StateMachine.add('MapCommand', Map(), transitions={'success':'WaitingForOrders'})
    
    #"sis" solo sirve para mostrar una representación gráfica de la máquina de estados    
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    sm.execute()
    rospy.spin()
    sis.stop()
