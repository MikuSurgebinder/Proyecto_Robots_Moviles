# -*- coding: utf-8 -*-
# from __future__ import print_function

import rospy
import smach_ros
import math
from smach import State,StateMachine
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist
from color_detector import ColorDetector

TOPIC_VEL = "/cmd_vel"
TOPIC_SCAN = '/base_scan'


#Nos fijamos en el ángulo a 30 y -30 grados, podéis cambiarlo si quereis
ANG_IZQ = 30*math.pi/180.0
ANG_DER = -ANG_IZQ


class FollowYellowAndEvade(State):
    def __init__(self):
        #State.__init__(self, outcomes=['color_detected'])
        self.color_detected = False
        self.pub = rospy.Publisher(TOPIC_VEL, Twist, queue_size=5)
        self.area = 50000
        self.dist_izq = 1
        self.dist_der = 1
        self.dist_fron = 1
    
    def navig(self):
        cd  = ColorDetector() #iniciamos el color detector
        self.subScan = rospy.Subscriber(TOPIC_SCAN, LaserScan, self.laser_callback)
        self.seguimiento_sub = rospy.Subscriber('/color_detected', Int32MultiArray, self.callback_seguimiento) 
        rate = rospy.Rate(10)
        rate.sleep()

        #return "color_detected" #cuando lo detecte directamente se cambia de estado 
        
    def laser_callback(self,msg):
        #cuáles son los rayos de laser que nos interesan?
        pos_izq = int((ANG_IZQ-msg.angle_min))#/msg.angle_increment)
        pos_der = int((ANG_DER-msg.angle_min))#/msg.angle_increment) 
        #FALTA: calcular la velocidad angular en z y lineal en x adecuadas a las distancias detectadas
        self.dist_izq = min(msg.ranges[pos_izq],msg.ranges[len(msg.ranges)-1])
        #print(pos_izq)
        self.dist_der = min(msg.ranges[pos_der],msg.ranges[0])
        self.dist_fron = msg.ranges[int(len(msg.ranges)/2)]

    def callback_seguimiento(self, msg):
        [self.area, self.dist_x, self.dist_y] = msg.data
        #print("Izq", self.dist_izq, " Der: ", self.dist_der)
        cmd = Twist()
        
        ########################################################################################
        #Avanzamos en funcion de que distancia es mayor: Hay mas hueco izq, vamos para alla
        #Con este planteamiento navega bien en general, sobre todo va en linea recta.
        #Aunque hay que echarle una mano porque en ocasiones se lanza contra la pared o
        #se queda encerrado en el cuadrado de salida estrecha.

        #Variables para escapar de cajas con salidas estrechas, recordamos ultima pared.
        #ult_izq= False
        #ult_der = False
        
        #Distancia máxima para acercarse al obstáculo
        dist_obst = 0.3
        #Izq y derecha están lejos de una colision, da igual la cmd.angular
        if self.dist_fron > dist_obst*3 and not(self.dist_izq < dist_obst or self.dist_izq < dist_obst):
            if self.area >40000 :
                cmd.linear.x = 0.0
            else:
                #velocidad proporcional a la distancia al seguimiento
                cmd.linear.x = 20000/self.area
        
        cmd.angular.z = -self.dist_x*abs(self.dist_x)/10000 -self.dist_x/300
        
        """
        if self.dist_izq < dist_obst:
            cmd.angular.z = cmd.angular.z*2
        elif self.dist_der > dist_obst:
            cmd.angular.z = cmd.angular.z*2
        """
        """
        #Detectamos a la izq, giramos derecha
        elif dist_izq < dist_obst:
            cmd.linear.x = 0.15
            cmd.angular.z = -1.2
            #ult_izq = True
            #ult_der = False
        #Detectamos a la der, giramos izquierda
        elif dist_der < dist_obst:
            cmd.linear.x = 0.15
            cmd.angular.z = 1.2
            #ult_izq = False
            #ult_der = True
        #Ambos detectan: se retrocede
        else:
            if(dist_izq < dist_obst):
                cmd.linear.x = -0.7
                cmd.angular.z = -0.8
            if(dist_der < dist_obst):
                cmd.linear.x = -0.7
                cmd.angular.z = 0.8
        if(dist_izq < 0.2 and dist_der < 0.2):
            cmd.linear.x = -1.0
            cmd.angular.z = 0.0
        """
        self.pub.publish(cmd)

    def close(self):
        self.seguimiento_sub.unregister()
        self.subScan.unregister()



"""
#En el proyecto no hay que usar este main
if __name__ == '__main__':
    global rojo
    rospy.init_node("practica3")
    sm = StateMachine(outcomes=['end'])
    with sm:
        #en la versión final la transición deberá ser al estado "volver a la base"
        StateMachine.add('WanderAndDetect', WanderAndDetect(), 
           transitions={
               'color_detected':'end'}) 
    
    sis = smach_ros.IntrospectionServer('server_name', sm, '/SM_ROOT')
    sis.start()
    sm.execute()
    rospy.spin()   
"""