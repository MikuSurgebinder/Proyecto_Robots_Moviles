#Proyecto - Robots moviles
#Esta es la base: utilizamos los programas de SLAM de ROS para que el robot cree el mapa: solamente lo hace una vez

#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import math, rospy
from visualization_msgs.msg import Marker, MarkerArray
from sensor_msgs.msg import LaserScan
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import Point
from geometry_msgs.msg import PointStamped
 

UMBRAL = 2 #basado en la distancia que mas o menos hay de margen (en unidades)
Z = 0   #En general la altura va a ser siempre 0 porque es un mapa en 2D

#No se ha modificado nada de esta funcion. 
def crear_marker(pos, id):
    marker = Marker()
    marker.header.frame_id = "map"  # Sistema de coordenadas de referencia
    marker.header.stamp = rospy.Time.now()
    marker.ns = "landmarks"  # Namespace
    marker.id = id  # Identificación única de cada marcador
    marker.type = Marker.SPHERE  # Tipo de marker (esfera para el landmark)
    marker.action = Marker.ADD
    # Posición del landmark
    marker.pose.position.x = pos[0]
    marker.pose.position.y = pos[1]
    marker.pose.position.z = pos[2]
    # Orientación del landmark
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    # Escala del marker (tamaño)
    marker.scale.x = 0.5
    marker.scale.y = 0.5
    marker.scale.z = 0.5
    # Color del marker (RGB + Alpha)
    marker.color.r = 1.0 
    marker.color.g = 1.0
    marker.color.b = 1.0
    marker.color.a = 1.0  # Transparencia
    # Duración (0 significa que será permanente)
    marker.lifetime = rospy.Duration(0)
    return marker


#Se ha modificado esta funcion para añadir 
def callback_laser(msg):
    global tfBuffer
    global positions #Las posiciones son globales para que no se borren
    nrayos = len(msg.ranges)
    for index in range(1, nrayos): #nos saltamos uno para tener siempre un rayo anterior para comparar
        dist_ant = msg.ranges[index - 1]
        dist  = msg.ranges[index]
        if dist<dist_ant-UMBRAL:
            #el angulo se obtiene con el angulo minimo captado + el num de captacion que es
            angulo = msg.angle_min + index*msg.angle_increment 
            lect_x = dist*math.cos(angulo)
            lect_y = dist*math.sin(angulo)

            try:
                #Obtener la transformación entre un sistema "padre" e "hijo". #Time(0) indica que queremos la última disponible
                transf = tfBuffer.lookup_transform('map', 'base_laser_link', rospy.Time(0))
                pnto = Point(lect_x, lect_y, Z)
                pointStamped = PointStamped(point = pnto)
                pnto_transf = tf2_geometry_msgs.do_transform_point(pointStamped, transf)
                ya_esta = False
                #vamos a ver si se ve
                print(pnto_transf)
                for i in range(0, len(positions)):
                    if (abs(positions[i][0]-pnto_transf.point.x) < UMBRAL) and (abs(positions[i][1]-pnto_transf.point.y) < UMBRAL):
                        ya_esta = True
                if not ya_esta:
                    positions.append((pnto_transf.point.x, pnto_transf.point.y, Z))
            #si se da alguna de estas excepciones no se ha podido encontrar la transformación    
            except (tf2_ros.LookupException, tf2_ros.ConnectivityException, tf2_ros.ExtrapolationException):
                rospy.logerr("No se ha podido encontrar la transformación")

# Hasta aqui modificar solo lo de arriba !!!!!
#------------------------------------------------------------------------------------------------------------

    # crear y publicar el mapa con los landmarks. En ROS podemos representar un landmark con un Marker
    # un marker array no es más que una lista de landmarks
    marker_array = MarkerArray()
    # Definir posiciones para los landmarks. De momento son fijas
    # Tendréis que sacarlas de los datos del laser
    # ADEMÁS habrá que transformar las coordenadas de los landmark
    # que serán relativas al robot  ('base_laser_link') al sistema 'map'

    for i, pos in enumerate(positions):
        # Añadir el marcador al MarkerArray 
        marker_array.markers.append(crear_marker(pos,i))

    # Publicar el MarkerArray
    marker_pub.publish(marker_array)

    
#Inicializar el vector de posiciones, es global -_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_
rospy.init_node('Mapeado_landmarks')
positions = [
    ]
sub = rospy.Subscriber('/base_scan', LaserScan, callback_laser)
marker_pub = rospy.Publisher('/mapa_landmarks', MarkerArray, queue_size=10)
#el tfBuffer es el que nos servirá para transformar las coordenadas de un sistema a otro
tfBuffer = tf2_ros.Buffer()
# para que el tfBuffer funcione es necesario inicializar este listener aunque luego no lo usaremos directamente
listener = tf2_ros.TransformListener(tfBuffer)

rospy.spin()


#Info extra
    #Este print (de Python 3) 
    #print('más lejano:', masLejano, ' x:', lect_x, ' y:', lect_y) 