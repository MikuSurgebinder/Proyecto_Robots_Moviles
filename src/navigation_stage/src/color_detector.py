# -*- coding: utf-8 -*-
# from __future__ import print_function
import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import String, Int32


UMBRAL_PIXELS = 100 #Cantidad de pixeles rojos a detectar para mandar la señal

class ColorDetector: #Clase/función para la detección de rojo. Si detecta, publica en /color_detected
    
    def __init__(self):
        self.bridge = cv_bridge.CvBridge() #Coger la camara de la simulación
        self.pub = rospy.Publisher('/color_detected', Int32, queue_size=5) #Prepara publicación en el topic de salida y
        self.image_sub = rospy.Subscriber('/image', Image, self.image_callback) #suscripción a la camara
        

    def image_callback(self, msg):
        
        cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8") #Captura de imagen y formateo para procesado
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0,50,50]) #Rango de rojos
        upper_red = np.array([10,255,255])

        mask = cv2.inRange(hsv, lower_red, upper_red) #Binarización al umbral seleccionado (tonos de rojo)

        cv2.imshow("Image window", mask) #Visualización de la binarización
        cv2.waitKey(3)

        pixels_detectados = cv2.countNonZero(mask) #Si la cantidad de pixeles blancos (rojo binarizado)
        if pixels_detectados>UMBRAL_PIXELS:        #excede el umbral,
            #print("Detectados: ", pixels_detectados)
            self.pub.publish(1)                    #Publica en el topic de salida
            self.image_sub.unregister()            #y finaliza la suscripción para evitar el consumo de recursos

if __name__ == '__main__':  #Para testeo
    rospy.init_node('color_detector')
    cd  = ColorDetector()
    rospy.spin()       