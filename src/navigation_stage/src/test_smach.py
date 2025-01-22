from __future__ import print_function

import rospy
import smach_ros
import math
from smach import State,StateMachine
from time import sleep
from turtlebot_band_detection import TurtleCamProcessor
from std_msgs.msg import String, Int32MultiArray

from handyFunctions import split_input,get_localization, moverse

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

#Para almacenar los datos recibidos de la interfaz, guarda si es una pulsacion larga o corta
#Una vez se ejecuta la accion, se reinicia a None
saved_buttons = {
    'B0': None, 'B1': None, 'B2': None,  # Physical buttons
    'D3': None, 'D4': None, 'D5': None,   # Digital buttons
    'WAIT': None
}
#Para poder trabajar más cómodamente entre estados
current_button = ''


#Almacena las poses a las que se le puede pedir ir al robot
position = {
    'B0': None, 'B1': None, 'B2': None,  # Physical buttons
    'D3': None, 'D4': None, 'D5': None,   # Digital buttons
}


class Static(State):
    def __init__(self):
        State.__init__(self, outcomes=['buttonPressed','followPerson','mapping'])
    
    def execute(self, userdata):
        global current_button
        #Velocidad=0 y pub

        print("Estado parado")
        while not rospy.is_shutdown():
            #Boton de follow
            if saved_buttons['WAIT'] is not None:
                saved_buttons['WAIT']=None
                return 'followPerson'
            
            #Botones de pose
            elif saved_buttons['B0'] is not None: 
                current_button = 'B0'
                return 'buttonPressed'
            elif saved_buttons['B1'] is not None: 
                current_button = 'B1'
                return 'buttonPressed'
            elif saved_buttons['B2'] is not None: 
                current_button = 'B2'
                return 'buttonPressed'
            elif saved_buttons['D3'] is not None: 
                current_button = 'D3'
                return 'buttonPressed'
            elif saved_buttons['D4'] is not None: 
                current_button = 'D4'
                return 'buttonPressed'
            elif saved_buttons['D5'] is not None: 
                current_button = 'D5'
                return 'buttonPressed'
                
            """
            if 'echo en callback de mapeado'==True:
                return 'mapping'
            """


class Button(State): #Funcion para guardar/ir a posición guardada
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        global current_button
        print("BOTON pulsado  " + current_button + "  " + saved_buttons[current_button])
        #Almacena
        if saved_buttons[current_button]== 'long':
            position[current_button] = get_localization() #Coge la pose del odom y la almacena
        #Se mueve
        elif saved_buttons[current_button]== 'short' and position[current_button] is not None:
            moverse(position[current_button])
        elif position[current_button] is None:
            rospy.loginfo("No hay una pose asociada a este botón")
        saved_buttons[current_button] = None
        current_button = ''
        return 'success'
        



class Follow(State): #Boton de WAIT pulsado
    def __init__(self):
        State.__init__(self, outcomes=['success'])
    
    def execute(self, userdata):
        bandera = False
        #processor = TurtleCamProcessor()
        #rospy.sleep(0.1)
        print("Estado camara seguimiento")

        def callback_seguimiento(msg):
            [area, dist_x, dist_y] = msg
            #Añadir algoritmo de movimiento con esquiva
            seguimiento_sub.unregister()

        seguimiento_sub = rospy.Subscriber('/color_detected', Int32MultiArray, callback_seguimiento) #Robot simulado
        rate = rospy.Rate(10)  # Procesa frames a 10 Hz
        
        while not rospy.is_shutdown() and not bandera:
            #processor.process_frame()
            
            if saved_buttons['WAIT'] is not None:
                saved_buttons['WAIT']=None
                bandera=True
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
