#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Librerías a usar
import rospy, cv2, cv_bridge
import numpy as np
#from sensor_msgs.msg import Int32
from sensor_msgs.msg import Image

AREA_MAXIMA = 15000
AREA_MINIMA = 500

class TurtleCamProcessor:
    def __init__(self):  # Inicialización de la clase
        # Crea una instancia del publicador del topic '/color_detected' que usa datos tipo Int32
        #self.pub = rospy.Publisher('/color_detected', Int32, queue_size=5)

        # Inicializa la cámara (0 para la cámara por defecto)
        #camera_index = 0  # Cambia este índice para usar otra cámara conectada
        #self.cap = cv2.VideoCapture(camera_index)
        self.area=0
        self.x_coord = 0
        self.y_coord = 0
        self.msg = 0
        self.bridge = cv_bridge.CvBridge()
        self.image_sub = rospy.Subscriber('/image', Image, self.callback_cam)

    def callback_cam(self,msg):
        self.msg=msg

    def process_frame(self):
        
        frame = self.bridge.imgmsg_to_cv2(self.msg, "bgr8") #Pasar de msg a imagen

        # Quitar el efecto espejo (volteo horizontal)
        frame_no_mirror = cv2.flip(frame, 1)

        # Calculo de luminosidad normalizada
        gray = cv2.cvtColor(frame_no_mirror, cv2.COLOR_BGR2GRAY)
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
        hsv = cv2.cvtColor(frame_no_mirror, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([25, 100, umbral_d])  # Rango mínimo de amarillo ajustado
        upper_yellow = np.array([35, 255, umbral_u])  # Rango máximo de amarillo ajustado
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

        # Aplicar la máscara y detectar contornos
        yellow_banda = cv2.bitwise_and(frame_no_mirror, frame_no_mirror, mask=mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_area = 0
        largest_contour = None

        for contour in contours:
            area = cv2.contourArea(contour)
            if AREA_MINIMA < area < AREA_MAXIMA:  # Area dentro de umbrales
                if area > max_area:
                    max_area = area
                    largest_contour = contour

        if largest_contour is not None:
            x, y, w, h = cv2.boundingRect(largest_contour)
            cv2.rectangle(yellow_banda, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.drawContours(yellow_banda, [largest_contour], -1, (0, 0, 255), 2)
            center_x = x + w // 2
            center_y = y + h // 2
            cv2.circle(yellow_banda, (center_x, center_y), 5, (0, 0, 255), -1)
            #rospy.loginfo(f'Area: {max_area}, x: {x}, y: {y}')

            cv2.imshow('Banda Amarilla Detectada', yellow_banda)
            self.area=max_area
            self.x_coord = x
            self.y_coord = y
            #return (max_area,x,y)  # Publica el área detectada en el topic
        cv2.imshow('Banda Amarilla Detectada', frame_no_mirror)#yellow_banda)




    def cleanup(self):
        #self.cap.release()
        cv2.destroyAllWindows()
        rospy.signal_shutdown("Cerrando TurtleCamProcessor.")

if __name__ == '__main__':
    rospy.init_node('turtle_cam_processor')  # Nombre del nodo
    processor = TurtleCamProcessor()

    try:
        rate = rospy.Rate(10)  # Procesa frames a 10 Hz
        while not rospy.is_shutdown():
            processor.process_frame()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
    finally:
        processor.cleanup()