from tkinter import *
import tkinter as tk
import os
import subprocess
from subprocess import check_call
from tkinter.ttk import *
from time import strftime
import psutil


#path to phototrap code
python_path = "/home/pi/Desktop/pitoniktest.py"


#opening phototrap on startup raspberry
subprocess.Popen(["python3",python_path])


#opening folder with clips
def open_folder():
    folder_path = "records"
    subprocess.Popen(["xdg-open",folder_path])
    
#function to run phototrap if it isnt working
def run_program():
    p = subprocess.Popen(["python3",python_path])
    
#function to kill process of phototrap
def end_program():
    namex = "pitoniktest.py"
    check_call(["pkill", "-f", "pitoniktest.py"])





root = tk.Tk()
window = root

bg = PhotoImage(file = "/home/pi/Desktop/bg.png")

# Create Canvas
canvas1 = Canvas( root, width = 400,
				height = 400)

canvas1.pack(fill = "both", expand = True)

# Display image
canvas1.create_image( 0, 0, image = bg,
					anchor = "nw")

# Add Text
canvas1.create_text( 200, 250, text = "Welcome")

# Create Buttons
button1 = Button( root, text = "Exit", command=root.destroy)

button3 = Button( root, text = "Start", command=run_program)

button2 = tk.Button(window, text="otworz folder", command=open_folder)

button4 = Button( root, text = "Reset",command=end_program)

# Display Buttons
button1_canvas = canvas1.create_window( 100, 10,
									anchor = "nw",
									window = button1)

button2_canvas = canvas1.create_window( 100, 40,
									anchor = "nw",
									window = button2)

button3_canvas = canvas1.create_window( 100, 70, anchor = "nw",
									window = button3)

button4_canvas = canvas1.create_window( 100, 100,
									anchor = "nw",
									window = button4)


#clock is only for "art", because it looks very funny ;)
def clock():
    string = strftime('%H:%M:%S')
    lbl.config(text=string)
    lbl.after(1000,clock)
    
    
lbl=Label(root, font=('calbri',40,'bold'),
          background='red',
          foreground='white')

lbl.pack(anchor='center')
clock()

# Execute tkinter
root.mainloop()
