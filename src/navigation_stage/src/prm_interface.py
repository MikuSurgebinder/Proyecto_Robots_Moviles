#Proyecto - Robots moviles

#Este módulo implementa la interfaz. De momento muestra los 3 botones compartidos con los reales (B0,B1,B2) y los tres extra digitales (D3,D4,D5)
#D3 -> 
#B4 -> Si los mantienes pulsados 2 segundos, sobreescriben la pose. (implementado en máquina de estados)
#B5 -> 

#Añadimos 3 botones extra por digital mediante la interfaz de python.
#Básicamente al clicar un boton se publica en su topic como "pressed" para luego con la maq estados para ver si >2seg


#De momento solo imprime cosas por pantalla?

import rospy
import tkinter as tk
from time import time
from std_msgs.msg import Bool
from geometry_msgs.msg import Pose
from threading import Thread

# Global variables for storing positions
saved_positions = {'B0': None, 'B1': None, 'B2': None}
button_press_times = {'B0': None, 'B1': None, 'B2': None}

# Constants
LONG_PRESS_THRESHOLD = 2.0  # seconds

# Callback to detect hardware button presses
def button_callback(data, button_name):
    global button_press_times, saved_positions

    current_time = time()
    if data.data:  # Button is pressed
        if button_press_times[button_name] is None:
            button_press_times[button_name] = current_time
    else:  # Button is released
        if button_press_times[button_name] is not None:
            press_duration = current_time - button_press_times[button_name]
            if press_duration >= LONG_PRESS_THRESHOLD:
                rospy.loginfo(f"Long press detected for {button_name}")
                # Save current robot position if long press
                save_position(button_name)
            button_press_times[button_name] = None

def save_position(button_name):
    # Get the robot's current position and save it
    # In practice, you would get this from the robot's odometry or pose
    current_position = Pose()  # This would be replaced by actual robot pose retrieval
    saved_positions[button_name] = current_position
    rospy.loginfo(f"Saved position for {button_name}")

def move_to_position(button_name):
    # This would be replaced with actual robot movement to a saved position
    if saved_positions[button_name]:
        rospy.loginfo(f"Moving to saved position for {button_name}")
    else:
        rospy.logwarn(f"No saved position for {button_name}")

def create_ros_subscribers():
    # Subscribe to the button presses (simulating them for this example)
    rospy.Subscriber("/button_B0", Bool, button_callback, "B0")
    rospy.Subscriber("/button_B1", Bool, button_callback, "B1")
    rospy.Subscriber("/button_B2", Bool, button_callback, "B2")

def digital_button_click(button_name):
    # This simulates a digital button press for D3, D4, D5 in the GUI
    rospy.loginfo(f"Digital button {button_name} clicked!")
    if saved_positions[button_name]:
        move_to_position(button_name)
    else:
        rospy.logwarn(f"No saved position for {button_name}")

# GUI using Tkinter to simulate D3, D4, D5 buttons
def create_gui():
    def on_digital_button_click(button_name):
        # Simulate a click for digital buttons
        digital_button_click(button_name)

    # Setup Tkinter window
    root = tk.Tk()
    root.title("Turtlebot2 Control Interface")

    # Create digital buttons D3, D4, D5
    button_d3 = tk.Button(root, text="D3", width=10, command=lambda: on_digital_button_click('D3'))
    button_d3.pack(pady=10)

    button_d4 = tk.Button(root, text="D4", width=10, command=lambda: on_digital_button_click('D4'))
    button_d4.pack(pady=10)

    button_d5 = tk.Button(root, text="D5", width=10, command=lambda: on_digital_button_click('D5'))
    button_d5.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()

def main():
    rospy.init_node("turtlebot_interface", anonymous=True)

    # Create ROS subscribers
    create_ros_subscribers()

    # Start the Tkinter GUI in a separate thread so it doesn't block ROS
    gui_thread = Thread(target=create_gui)
    gui_thread.start()

    rospy.spin()


if __name__ == "__main__":
    main()
