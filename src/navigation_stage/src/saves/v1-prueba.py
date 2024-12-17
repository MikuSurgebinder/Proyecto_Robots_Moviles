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
saved_positions = {
    'B0': None, 'B1': None, 'B2': None,  # Physical buttons
    'D3': None, 'D4': None, 'D5': None   # Digital buttons
}
button_press_times = {'B0': None, 'B1': None, 'B2': None}
button_first_press_times = {'B0': None, 'B1': None, 'B2': None}
previous_time = time()

# Constants
LONG_PRESS_THRESHOLD = 2.0  # seconds

# Font configuration
font = ('Comic Sans MS', 12)  # Font for all buttons

def create_ros_subscribers(button_widgets):
    rospy.Subscriber("/button_B0", Bool, lambda data: button_callback(data, "B0", button_widgets))
    rospy.Subscriber("/button_B1", Bool, lambda data: button_callback(data, "B1", button_widgets))
    rospy.Subscriber("/button_B2", Bool, lambda data: button_callback(data, "B2", button_widgets))
    # Cannot subscribe to the digital ones unless we also create them topics

# Callback to detect hardware button presses
def button_callback(data, button_name, button_widgets):
    global button_press_times, saved_positions, button_first_press_times

    current_time = time()

    # Debug log to check if we are receiving button press events
    rospy.loginfo(f"Received {button_name} state: {data.data}")

    if data.data:  # Button is pressed
        if (current_time - previous_time ) :
            button_widgets[button_name].config(bg='red')
    else:  # Button is released
        if button_press_times[button_name] is not None: # The earlier state was pressed 
            press_duration = current_time - button_first_press_times[button_name] # The duration
            rospy.loginfo(f"Button {button_name} released. Press duration: {press_duration:.2f} seconds")

            if press_duration >= LONG_PRESS_THRESHOLD:
                rospy.loginfo(f"Long press detected for {button_name}")
                # Save current robot position if long press
                save_position(button_name)
            else:
                rospy.loginfo(f"Short press detected for {button_name}")

            # Reset button color to default
            button_widgets[button_name].config(bg='green')
        
        button_press_times[button_name] = None  
    previous_time = current_time

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

def create_ros_subscribers(button_widgets):
    # Subscribe to the button presses (simulating them for this example)
    rospy.Subscriber("/button_B0", Bool, button_callback, "B0", button_widgets)
    rospy.Subscriber("/button_B1", Bool, button_callback, "B1", button_widgets)
    rospy.Subscriber("/button_B2", Bool, button_callback, "B2", button_widgets)

def digital_button_click(button_name):
    # This simulates a click for digital buttons D3, D4, D5 in the GUI
    rospy.loginfo(f"Digital button {button_name} clicked!")
    if saved_positions[button_name]:
        move_to_position(button_name)
    else:
        rospy.logwarn(f"No saved position for {button_name}")

# GUI using Tkinter to simulate D3, D4, D5 buttons and display real buttons
def create_gui():
    # Create Tkinter window
    root = tk.Tk()
    root.title("Turtlebot2 Control Interface")

    # Create widgets for the real buttons (B0, B1, B2)
    button_widgets = {}  # To store button references

    # Function to change the state of digital buttons
    def on_digital_button_click(button_name):
        # Simulate a click for digital buttons
        digital_button_click(button_name)

    # Physical button setup with Comic Sans font
    button_widgets['B0'] = tk.Button(root, text="B0", width=10, bg='green', font=font, command=lambda: on_digital_button_click('B0'))
    button_widgets['B0'].pack(pady=10)

    button_widgets['B1'] = tk.Button(root, text="B1", width=10, bg='green', font=font, command=lambda: on_digital_button_click('B1'))
    button_widgets['B1'].pack(pady=10)

    button_widgets['B2'] = tk.Button(root, text="B2", width=10, bg='green', font=font, command=lambda: on_digital_button_click('B2'))
    button_widgets['B2'].pack(pady=10)

    # Digital button setup (D3, D4, D5) with Comic Sans font
    button_d3 = tk.Button(root, text="D3", width=10, font=font, command=lambda: on_digital_button_click('D3'))
    button_d3.pack(pady=10)

    button_d4 = tk.Button(root, text="D4", width=10, font=font, command=lambda: on_digital_button_click('D4'))
    button_d4.pack(pady=10)

    button_d5 = tk.Button(root, text="D5", width=10, font=font, command=lambda: on_digital_button_click('D5'))
    button_d5.pack(pady=10)

    # Run the Tkinter event loop
    root.mainloop()

    return button_widgets

def main():
    #global (data y tiempo-data)

    rospy.init_node("turtlebot_interface", anonymous=True)
    # Create Tkinter GUI and get the button widgets
    button_widgets = create_gui()
    # Create ROS subscribers to update the physical button states
    create_ros_subscribers(button_widgets)

    while not rospy.is_shutdown():
        rospy.sleep(1)
        #detectar oulsado y soltado con tiempo-data
        if (pulsado and tiempo-actual - tiempo-previo > 0.1): #up
            guaradar tiempo actual

        if (not pulsado and tiempo-actual - tiempo-previo > 0.1): #down
            if(tiempo-actual - tiempo-previo > LONG_PRESS_THRESHOLD and pulsado):
                true largo -> guardar posicion
            else:
                true corto, asi que voy
            

if __name__ == "__main__":
    main()
