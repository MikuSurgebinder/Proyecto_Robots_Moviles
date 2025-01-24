###----------------GUIA DE USO----------------###
El proyecto de git tiene las ramas estruturadas de manera que en todas hay informacion sobre las ramas en la raíz y hay una carpeta src para trabajar cómodamente donde esta todo el proyecto.
Para vincularlo, lo que hemos hecho ha sido clonar el repositorio de git donde se quiera y luego en un workspace precreado crear un acceso directo al src del git. De esta manera ros detecta el acceso directo como la carpeta src, pudiendo cambiar de rama y trabajando en la nueva sin tener que preocuparnos por el formato.
El código principal esta en la rama main.

#Cómo ejecutar el código:#
1. Abrir el workspace y hacer un catkin_make y un source devel/setup.bash
2. Ejecutar roslaunch navigation_stage mi_navigation.launch
3. En nuevas terminales ejecutar los códigos:
	- python3 turtlebot_band_detection_real.py (este programa se queda en segundo plano hasta que la máquina de estados se lo indique)
	- python3 interfaz.py (este programa es la interfaz con botones para el usuario)
	- python3 maquina_estados.py (el main, la maquina de estados que gestiona las peticiones)
	
	
#Cómo usar el código:#
En la interfaz se puede estar en dos modos:
	- Modo seguimiento: este módo sigue al objeto amarillo (cubo en este caso) el cual se puede activar y detener con el botón "WAIT"
	- Modo navegación automática: en este modo se pueden guardar posiciones o hacer que el robot vaya a una posición automáticamente. Una pulsación larga hará que el robot guarde su posición actual, mientras que una corta hará que vaya al lugar guardado previamente.

Si se pulsa un botón mientras está el modo seguimiento activo no sucederá nada, ya que en la vida real los botones se encuentran en el turtlebot y acercarse tanto a la banda a detectar puede suponer un problema, por tanto es necesario detener el robot previamente. Así mismo, para llevar al robot a un sitio es necesario detener al robot, ya que se desea evitar que se desconozca si se ha dejado el seguimiento activo o no y el robot dejará de estar supervisado, pudiendo esto causar problemas.
