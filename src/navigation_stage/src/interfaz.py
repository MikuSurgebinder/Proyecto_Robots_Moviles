#Proyecto - Robots moviles

# We have 3 real buttons, which can also be actuated by the interface. Plus 3 digital only. And we added one button to toggle "Wait/Follow command"
# In total: 6 position buttons + 1 instruction button. The postition ones recognise short/long presses

#TO IMPLEMENT: WHEN PRESSED REAL B0&B1 SIMMULTANEOUSLY, switch bool "WAIT" - - - WE NEED THE REAL TOPICS



# TO IMPLEMENT NOW: CREAR TOPIC PARA LA INTERFAZ, donde pasar los nombres y tal de los botones y su estado

# TOPICS
import rospy
import tkinter as tk
from time import time
from std_msgs.msg import Bool, String
from geometry_msgs.msg import Pose
from threading import Thread

# Global variables for storing positions
saved_positions = {
    'B0': None, 'B1': None, 'B2': None,  # Physical buttons
    'D3': None, 'D4': None, 'D5': None,   # Digital buttons
    'WAIT': None
}
previous_press = {'B0': None, 'B1': None, 'B2': None, 
                  'D3': None, 'D4': None, 'D5': None,
                  'WAIT': None} 
actual_press = {'B0': None, 'B1': None, 'B2': None, 
                'D3': None, 'D4': None, 'D5': None,
                  'WAIT': None} 

previous_time = time()
#current_time = time() #we'll innitialize this one when needed

# Constants
LONG_PRESS_THRESHOLD = 1.0  # seconds

# Font configuration
font = ('Comic Sans MS', 12)  # Font for all buttons



def create_ros_subscribers(button_widgets):
    rospy.Subscriber("/button_B0", Bool, lambda data: button_callback(data, "B0", button_widgets)) # For the real buttons, not just the interface
    rospy.Subscriber("/button_B1", Bool, lambda data: button_callback(data, "B1", button_widgets))
    rospy.Subscriber("/button_B2", Bool, lambda data: button_callback(data, "B2", button_widgets))
    # Cannot subscribe to the digital ones unless we also create them topics

# Callback to detect hardware button presses
def button_callback(data, button_name, button_widgets):
    global previous_press, actual_press, saved_positions, previous_time

    current_time = time()

    # Debug log to check if we are receiving button press events
    rospy.loginfo(f"Received {button_name} state: {data.data}")

    if data.data:  # Button is pressed
        if (current_time - previous_time):
            button_widgets[button_name].config(bg='red')
    else:  # Button is released
        if previous_press[button_name] is not None: # The earlier state was pressed 
            press_duration = current_time - previous_time[button_name] # The duration
            previous_press[button_name] = data.data
            rospy.loginfo(f"Button {button_name} released. Press duration: {press_duration:.2f} seconds")

            if press_duration >= LONG_PRESS_THRESHOLD:
                # rospy.loginfo(f"Long press detected for {button_name}")
                # publish button_name and long                #---------------------------------------------------------*******************
                # Save current robot position if long press
                save_position(button_name)
            else:
                rospy.loginfo(f"Short press detected for {button_name}") # comment this later
                # publish button_name and long                #---------------------------------------------------------*******************

            # Reset button color to default
            button_widgets[button_name].config(bg='green')
        
        actual_press[button_name] = None  # Release all buttons
    previous_time = time()

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

#-------------------------------------------------------------------------------------------------------------- I N T E R F A C E --------#
# GUI using Tkinter to simulate D3, D4, D5 buttons and display real buttons
def create_gui():
    # Create Tkinter window
    root = tk.Tk()
    root.title("Turtlebot2 Control Interface")

    # Publishers
    pub_buttons = rospy.Publisher("/button_communication", String, queue_size=10)

    # Dictionary to store button press times
    button_press_times = {
        'B0': None, 'B1': None, 'B2': None,  # Physical buttons
        'D3': None, 'D4': None, 'D5': None,   # Digital buttons
        'WAIT': None
    }

    # Helper functions for handling press and release
    def handle_button_press(button_name):
        rospy.loginfo(f"Button {button_name} pressed")
        button_press_times[button_name] = time()  # Record the press time

    def handle_button_release(button_name): #-------------------------------------------------add return to get variable if it was long/short press
        if button_press_times[button_name] is not None:
            press_duration = time() - button_press_times[button_name]
            #rospy.loginfo(f"Button {button_name} released after {press_duration:.2f} seconds")

            if press_duration >= LONG_PRESS_THRESHOLD:
                #rospy.loginfo(f"Long press detected for {button_name}")
                #   publish button name and long            #---------------------------------------------------------*******************
                save_position(button_name)
                out = button_name + ", long"
                pub_buttons.publish(out)
            else:
                #rospy.loginfo(f"Short press detected for {button_name}")
                #   publish button name and short           #---------------------------------------------------------*******************
                digital_button_click(button_name)
                out = button_name + ", short"
                pub_buttons.publish(out)

            button_press_times[button_name] = None  # Reset press time

    # Function to create circular buttons
    def create_circle_button(canvas, x, y, r, color, text, button_name):
        # Draw a circle
        button = canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, outline="black", width=2)

        # Add button text
        label = canvas.create_text(x, y, text=text, font=("Comic Sans MS", 14, "bold"), fill="black")

        # Bind press and release events to the circle
        canvas.tag_bind(button, "<ButtonPress>", lambda event: handle_button_press(button_name))
        canvas.tag_bind(button, "<ButtonRelease>", lambda event: handle_button_release(button_name))
        canvas.tag_bind(label, "<ButtonPress>", lambda event: handle_button_press(button_name))
        canvas.tag_bind(label, "<ButtonRelease>", lambda event: handle_button_release(button_name))

    class Rectangle_button():
        def __init__(self, canvas, x, y, w, h, color, text, button_name):
            self.x = x
            self.y = y 
            self.w = w
            self.h = h
            self.color = color
            self.text = text
            self.button_name = button_name
            self.canvas = canvas

            # Draw a rectangle
            self.button = canvas.create_rectangle(x, y, x+w, y+h, fill=color, outline="black", width=2)

            # Add button text
            self.label = canvas.create_text(x+w/2, y+h/2, text=self.text, font=("Comic Sans MS", 14, "bold"), fill="black")

            # Bind press and release events to the circle
            self.canvas.tag_bind(self.button, "<ButtonPress>", lambda event: handle_button_press(button_name))
            self.canvas.tag_bind(self.button, "<ButtonRelease>", lambda event: handle_button_release(button_name))
            self.canvas.tag_bind(self.label, "<ButtonPress>", lambda event: handle_button_press(button_name))
            self.canvas.tag_bind(self.label, "<ButtonRelease>", lambda event: handle_button_release(button_name))
        
        def change_rectangle_button(self, text=None, color=None):
            # Update text if provided
            if text:
                self.text = text
                self.canvas.itemconfig(self.label, text=self.text)  # Update existing text label

            # Update color if provided
            if color:
                self.color = color
                self.canvas.itemconfig(self.button, fill=self.color)  # Update rectangle color


    # Main canvas to hold circular buttons and labels
    canvas = tk.Canvas(root, width=350, height=450, bg='white')
    canvas.pack()

    # Add headings for each column
    canvas.create_text(100  , 50, text="Real Buttons", font=("Comic Sans MS", 14, "bold"), fill="black")
    canvas.create_text(250, 50, text="Digital Buttons", font=("Comic Sans MS", 14, "bold"), fill="black")

    # Create physical buttons (B0, B1, B2) as circles
    create_circle_button(canvas, x=100, y=120, r=40, color="yellow", text="B0", button_name='B0')
    create_circle_button(canvas, x=100, y=220, r=40, color="yellow", text="B1", button_name='B1')
    create_circle_button(canvas, x=100, y=320, r=40, color="yellow", text="B2", button_name='B2')

    # Create digital buttons (D3, D4, D5) as circles
    create_circle_button(canvas, x=250, y=120, r=40, color="cyan", text="D3", button_name='D3')
    create_circle_button(canvas, x=250, y=220, r=40, color="cyan", text="D4", button_name='D4')
    create_circle_button(canvas, x=250, y=320, r=40, color="cyan", text="D5", button_name='D5')

    # Create digital button WAIT                           #---------------------------------------------------------*******************
    wait_button = Rectangle_button(canvas, x=80, y=390, w=190, h=40, color="green", text="WAIT", button_name='WAIT')
    #rospy.sleep(2)
    #wait_button.change_rectangle_button(text="Follow", color="green")

    # Run the Tkinter event loop
    root.mainloop()


def main():
    #global (data y tiempo-data)
    current_time = time()

    rospy.init_node("turtlebot_interface", anonymous=True)
    # Create Tkinter GUI and get the button widgets
    button_widgets = create_gui()
    # Create ROS subscribers to update the physical button states
    create_ros_subscribers(button_widgets)

    while not rospy.is_shutdown():
        rospy.sleep(1)
        # ADD HERE TWO BUTTONS LOGIC FOR WAIT/FOLLOW IT HAS TO BE W/ REAL BUTTONS     #----------------------------------------*******************
        # Register status of both buttons and if coinciden pum

if __name__ == "__main__":
    main()
    rospy.sleep(1)