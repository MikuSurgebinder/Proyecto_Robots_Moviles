#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Librerías a usar
import rospy, cv2, cv_bridge
import numpy as np
from sensor_msgs.msg import Image
from std_msgs.msg import Int32MultiArray, String

AREA_MAXIMA = 50000
AREA_MINIMA = 50
camera_st=False
X_VENTANA=640
Y_VENTANA=480

class TurtleCamProcessor:
    def __init__(self):  # Inicialización de la clase
        # Crea una instancia del publicador del topic '/color_detected' que usa datos tipo Int32MultiArray
        self.pub = rospy.Publisher('/color_detected', Int32MultiArray, queue_size=5)
        self.bridge = cv_bridge.CvBridge() #Pasar de msg a imagen
        #Se suscribe al topic '/image' que usa datos tipo Image y cada vez que recibe un mensaje llama a la función process_frame
        self.image_sub = rospy.Subscriber('/image', Image, self.process_frame) #Robot simulado
        self.image_sub = rospy.Subscriber('/camera_onoff', String, self.desub_camera) #Robot real

    def process_frame(self,msg):
        global camera_st
        if camera_st:
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8") #Pasar de msg a imagen

            # Calculo de luminosidad normalizada
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            luminosidad_total = np.mean(gray)
            luminosidad_normalizada = (luminosidad_total / 255) * 100

            # Ajustar los umbrales dinámicamente según la luminosidad
            if 40 < luminosidad_normalizada < 70:  # luz intermedia
                umbral_d = 120
                umbral_u = 200
            elif luminosidad_normalizada > 70:  # Mucha luz
                umbral_d = 200
                umbral_u = 255
            else:  # poca luz
                umbral_d = 40
                umbral_u = 120

            # Convertir el frame a espacio de color HSV
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            lower_yellow = np.array([25, 100, umbral_d])  # Rango mínimo de amarillo ajustado
            upper_yellow = np.array([35, 255, umbral_u])  # Rango máximo de amarillo ajustado
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

            # Aplicar la máscara y detectar contornos
            yellow_banda = cv2.bitwise_and(frame, frame, mask=mask)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            #Si encuentra contorno:
            if contours is not None:
                msg_new = Int32MultiArray()
                max_area = 0
                largest_contour = None

                for contour in contours: #Se queda con el mayor contorno entre límites
                    area = cv2.contourArea(contour)
                    if AREA_MINIMA < area < AREA_MAXIMA:  # Area dentro de umbrales
                        if area > max_area: # Supera al máximo que ya se tiene
                            max_area = area
                            largest_contour = contour

                if largest_contour is not None:
                    #Dibujo del contorno
                    x, y, w, h = cv2.boundingRect(largest_contour)
                    cv2.rectangle(yellow_banda, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.drawContours(yellow_banda, [largest_contour], -1, (0, 0, 255), 2)
                    #Obtiene los centros sin decimales (importante)
                    center_x = x + w // 2
                    center_y = y + h // 2
                    #Pinta el círculo del 0,0
                    cv2.circle(yellow_banda, (center_x, center_y), 5, (0, 0, 255), -1)
                    #Imprime
                    distancia_x=-(X_VENTANA/2)+(x + w / 2)
                    distancia_y=-(Y_VENTANA/2)+(y + h / 2)
                    rospy.loginfo(f'Area: {max_area}, x: {distancia_x}, y: {distancia_y}')
                    msg_new.data = [int(max_area), int(distancia_x), int(distancia_y)] 
                    self.pub.publish(msg_new)  # Publica el área detectada en el topic
                
            cv2.imshow('Banda Amarilla Detectada', yellow_banda)
            cv2.waitKey(3)

    def desub_camera(self, msg): #Se le llama cada vez que la cámare lee un mensaje de /camera_onoff
        global camera_st
        if msg.data == "suscribe": #Si el mensaje es 'suscribe'
            camera_st=True
            rospy.loginfo("Suscribiéndonos al topic '/image'.") #Imprime la confirmación
            self.image_sub = rospy.Subscriber('/image', Image, self.process_frame) #Y se suscribe

        elif msg.data == "desuscribe": #Si el mensaje es 'desuscribe'
            camera_st=False
            rospy.loginfo("Desuscribiéndonos del topic '/image'.") #Imprime la confirmación
            self.image_sub.unregister()  #Y se desuscribe
            self.image_sub = None #Elimina el objeto

    def cleanup(self):
        self.image_sub.unregister()  #Y se desuscribe
        self.image_sub = None #Elimina el objeto

if __name__ == '__main__':
    rospy.init_node('turtle_cam_processor')  # Nombre del nodo
    
    try:
        rospy.loginfo("Esperando orden de inicialización") 
        processor = TurtleCamProcessor()
        rospy.spin() #Mantiene ROS en ejcución
    except rospy.ROSInterruptException:
        pass
    finally:
        processor.cleanup()
