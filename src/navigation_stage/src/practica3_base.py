# -*- coding: utf-8 -*-
# from __future__ import print_function

import rospy
import smach_ros
import math
from smach import State,StateMachine
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
from color_detector import ColorDetector

#Topics a usar en suscripciones y publicaciones
TOPIC_VEL = "/cmd_vel"
TOPIC_SCAN = '/base_scan'
TOPIC_COLOR = '/color_detected'


#Nos fijamos en el ángulo a 30 y -30 grados, podéis cambiarlo si quereis.
#Se ha añadido más adelante utilizar el haz frontal.
ANG_IZQ = 30*math.pi/180.0
ANG_DER = -ANG_IZQ


#Primer estado de la maquina de estados
class WanderAndDetect(State):

    def __init__(self):
        #State.__init__(self, outcomes=['color_detected']) #Como se acopla a la maquina principal, se desactivan cosas de la local
        print('Empieza a deambular') #Ver que empiece para debuggear
        State.__init__(self, outcomes=['success'])

        cd  = ColorDetector() #Ejecutar el programa de detección de rojo, en color_detector.py
        self.color_detected = False #Flag de finalización

        self.pub = rospy.Publisher(TOPIC_VEL, Twist, queue_size=5) #Para publicar la velocidad en el callback
    

    def execute(self, userdata):
        self.subScan = rospy.Subscriber(TOPIC_SCAN, LaserScan, self.laser_callback) #Inicializa los callbacks de laser y cámara
        self.subColor = rospy.Subscriber(TOPIC_COLOR, Int32 , self.color_detected_calback)
        rate = rospy.Rate(10)

        while not self.color_detected: #Entra en bucle de deambular hasta detectar rojo
            rate.sleep()

        #normalmente en un nodo de ROS convencional no nos desuscribimos
        #porque se hace automáticamente al acabar el nodo, pero esto es un estado
        #de la máquina de estados y mejor "limpiar" todo antes de saltar a otro estado
        
        
        if self.color_detected:       #Si detecta rojo:
            self.subScan.unregister() #Cancela los callbacks, deteniendo las acciones
            self.subColor.unregister()

        print("Termina deambular y va a casa")
        return 'success' #Termina el estado y da paso al siguiente
        
    
    def laser_callback(self, msg):
        #Se ha añadido una lectura más justo en frente para evitar colisiones
        pos_rec = int(len(msg.ranges)/2)
        pos_izq = int((ANG_IZQ-msg.angle_min)/msg.angle_increment)
        pos_der = int((ANG_DER-msg.angle_min)/msg.angle_increment) 
        #print("Izq", msg.ranges[pos_izq], " Der: ", msg.ranges[pos_der]) #Test

        #Guardamos valores de distancia para calcular velocidades optimas
        dist_rec = msg.ranges[pos_rec]
        dist_der = msg.ranges[pos_der]
        dist_izq = msg.ranges[pos_izq]


        #Creacion del mensaje para la determinar la velocidad (out)
        cmd = Twist()

        #Algoritmo de movimiento de deambular/wandering
        #cmd.linear.x= min([dist_rec,dist_der,dist_izq])*0.1-0.1 #Test
        cmd.linear.x= dist_rec*0.1
        cmd.angular.z=(dist_izq-dist_der)*0.13
        if abs(dist_rec)<0.5:
            cmd.linear.x = -0.5
            cmd.angular.z = -1
        
        #print("Avance", cmd.linear.x, " Giro: ", cmd.angular.z, " Espacio: " ,msg.ranges[pos_rec]) #Test

        self.pub.publish(cmd) #Publicar velocidad

    def color_detected_calback(self, msg):
        self.color_detected = True #Se publica en detectar rojo, levanta la bandera, parando el programa (Publicado en código color_detector.py)




if __name__ == '__main__': #Iniciar y ejecutar el estado/bucle hasta que cambie de estado, solo para debug
    rospy.init_node("practica3")

    #Maquina de estados local
    sm = StateMachine(outcomes=['end'])
    with sm:
        #en la versión final la transición deberá ser al estado "volver a la base"
        StateMachine.add('WanderAndDetect', WanderAndDetect(), 
           transitions={
               'success':'end'})
    
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    sm.execute()
    rospy.spin()   
