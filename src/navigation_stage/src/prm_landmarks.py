#Proyecto - Robots moviles

#Este módulo es para crear landmarks a petición desde el terminal indicando los numeritos
#pero también puede guardar la posición actual si se pulsa un botón del turtlebot >2s
#Eso se gestiona desde la maquina de estados, aqui se recibe la pose independientemente de:

#Topics que necesitamos:
    #botones ->  /mobile_base/events/button

#!/usr/bin/python
# -*- coding: utf-8 -*-
import rospy
import actionlib
import sys
from __future__ import print_function
import math, rospy
from visualization_msgs.msg import Marker, MarkerArray
from sensor_msgs.msg import LaserScan
import tf2_ros
import tf2_geometry_msgs
from geometry_msgs.msg import Point
from geometry_msgs.msg import PointStamped
from prm_buttons import buttons


def landmark(pose, id):
    #---POR TERMINAL---#
    if len(sys.argv) <= 2:
        print("Uso: " + sys.argv[0] + " x_objetivo y_objetivo")
        exit()      
    #---POR BOTÓN B0---#
    #Inicializamos los botones:
    buttons()
    #Configuramos el landmark
    marker = Marker()
    marker.header.frame_id = "map"  # Sistema de coordenadas de referencia
    marker.header.stamp = rospy.Time.now() 
    marker.ns = "landmarks"  # Namespace
    marker.id = id  # Identificación única de cada marcador
    marker.type = Marker.SPHERE  # Tipo de marker (esfera para el landmark)
    marker.action = Marker.ADD

    #Posición del landmark
    marker.pose.position.x 
    marker.pose.position.y 
    marker.pose.position.z = [0] #va a estar siempre en el suelo
    #Orientación del landmark por defecto siempre 
    marker.pose.orientation.x = 0.0
    marker.pose.orientation.y = 0.0
    marker.pose.orientation.z = 0.0
    marker.pose.orientation.w = 1.0
    #Escala del marker (tamaño)
    marker.scale.x = 0.5
    marker.scale.y = 0.5
    marker.scale.z = 0.5
    #Color del marker (RGB + Alpha)
    marker.color.r = 1.0 
    marker.color.g = 1.0
    marker.color.b = 1.0
    marker.color.a = 1.0  # Transparencia
    #Duración (0 significa que será permanente)
    marker.lifetime = rospy.Duration(0)
    return marker

#No se usa la funcion main en el programa como tal.
#if __name__ == "__main__":
