#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from __future__ import print_function

#Librerías a usar
import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String, Int32

UMBRAL_PIXELS = 100 #Variable global

class ColorDetector:
    def __init__(self): #Inicialización de la clase
        self.bridge = cv_bridge.CvBridge() #Pasar de msg a imagen
        #Crea una instancia del publicador del topic '/color_detected' que usa datos tipo Int32
        self.pub = rospy.Publisher('/color_detected', Int32, queue_size=5)
        #Se suscribe al topic '/image' que usa datos tipo Image y cada vez que recibe un mensaje llama a la función image_callback
        self.image_sub = rospy.Subscriber('/image', Image, self.image_callback)
        #Se suscribe a '/camera_onoff' que usa datos tipo Image y cada vez que recibe un mensaje llama a la función sub_callback
        self.stop_sub = rospy.Subscriber('/camera_onoff', String, self.sub_callback)

    def image_callback(self, msg): #Se le llama cada vez que la cámare lee un frame
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8") #Pasar de msg a imagen
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV) #cambio de representación de colores BGR=>HSV
        #Umbralización del color
        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        
        mask = cv2.inRange(hsv, lower_red, upper_red) #Crear una máscara que pone a 255 (blancos) los colores entre el rango (rojo)
        #También pone a 0 (negro) los colores fuera de rango
        pixels_detectados = cv2.countNonZero(mask) #CUenta los píxeles blancos (rojos)
        if pixels_detectados > UMBRAL_PIXELS: #Si superan un umbral de píseles
            print("Detectados: ", pixels_detectados) #Lo imprime por pantalla
            self.pub.publish(pixels_detectados) #Lo poblica en el topic

    def sub_callback(self, msg): #Se le llama cada vez que la cámare lee un mensaje de /camera_onoff
        rospy.loginfo(f"Recibido mensaje: {msg.data}") #Imprime el mensaje por pantalla
        if msg.data == "suscribe": #Si el mensaje es 'suscribe'
            if self.image_sub is None: #Y no está ya suscrito
                rospy.loginfo("Suscribiéndonos al topic '/image'.") #Imprime la confirmación
                self.image_sub = rospy.Subscriber('/image', Image, self.image_callback) #Y se suscribe

        elif msg.data == "desuscribe": #Si el mensaje es 'desuscribe'
            if self.image_sub is not None: #Y no está ya desuscrito
                rospy.loginfo("Desuscribiéndonos del topic '/image'.") #Imprime la confirmación
                self.image_sub.unregister()  #Y se desuscribe
                self.image_sub = None #Elimina el objeto

rospy.init_node('color_detector') #Nombre del nodo
cd = ColorDetector() #Llamada a la función principal
rospy.spin() #Mantiene ROS en ejcución
