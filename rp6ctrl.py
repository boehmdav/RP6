# This is a description!

# Imported Modules/Packages
import threading
from tkinter import *                   # GUI
import pygame                           # Used for controller-input
import sys                              #
from time import sleep
import os

# Some Defines
CANVAS_HEIGHT       = 50
CANVAS_WIDTH        = 100
CANVAS_BORDER_WIDTH = 2

# Global variables
end_intend = False
lock_end_intend = threading.Lock()
threads = []

axis = [0,0,0,0]
lock_axis = threading.Lock()

# Some checks
if CANVAS_WIDTH % 2 == 1:
    print("CANVAS_WIDTH is odd!")
    sys.exit()

class MyButton(Button):
    def destroy(self):
        global lock_end_intend, end_intend
        lock_end_intend.acquire()
        end_intend = True
        #print(end_intend)
        lock_end_intend.release()
        Button.destroy(self)
    
# The gui class - here is everything you see on the screen
class gui():
    def __init__(self, master):
        
        self.master = master
        
        # The Quit-Button
        MyButton(master, text="Exit", command=master.destroy, width=20).grid(row=3, column=3, columnspan=2)
        
        #The first bar (pitch)
        Label(master, text="Pitch: ").grid(row=0, column=0)
        
        self.canvas_pitch = Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#267F00")
        self.canvas_pitch.grid(row=0, column=1)
        
        self.rect_pitch = self.canvas_pitch.create_rectangle(CANVAS_WIDTH/2, 0, CANVAS_WIDTH/2, CANVAS_HEIGHT, fill="green")
        
        #The second bar (thrust)
        Label(master, text="Thrust: ").grid(row=1, column=0)
        
        self.canvas_thrust = Canvas(master, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="#267F00")
        self.canvas_thrust.grid(row=1, column=1)
        
        self.rect_thrust = self.canvas_thrust.create_rectangle(CANVAS_WIDTH/2, 0, CANVAS_WIDTH/2, CANVAS_HEIGHT, fill="green")
        
        #Console
        self.console = Text(master)
        self.console.grid(row=2,column=0,columnspan=2)
        self.console.bind("<KeyRelease>",self.console_key_release)
        self.console.bind("<KeyPress>",self.console_key_press)
        self.console.insert(END,"> ")
        self.console.focus()
        
        #Status window
        self.status = Label(master, text="Initial Text", height=32, width=20, anchor=NW, padx=5, pady=5)
        self.status.grid(row=0, column=2, columnspan=2, rowspan=3)
        
    def console_key_press(self, event):
        if event.keysym == 'Return':
            self.console.mark_set("insert", END)
    
    def console_key_release(self, event):
        last_line = int(self.console.index('end').split('.')[0])
        last_column = int(self.console.index('end').split('.')[1])
        line, column = self.console.index('insert').split('.')
        if (event.keysym == 'Right') or (event.keysym == 'Left') or (event.keysym == 'Up') or (event.keysym == 'Down'):
            if int(column) < 2:
                self.console.mark_set("insert", "%d.2" % (last_line-1))
            if (int(line)+1) != last_line:
                self.console.mark_set("insert", "%d.%d" % (last_line, last_column))
        elif event.keysym == 'Return':
            try:
                self.handle_input(self.console.get("%d.2"%(int(line)-1),"%d.end"%(int(line)-1)))
            except Exception:
                etype, evalue, etb = sys.exc_info()
                self.console.insert(END,"An error occured: %s%s"%(evalue,os.linesep))
            try:
                self.console.insert(END,"> ")
            except Exception:
                pass
    
    def handle_input(self, inp):
        if inp == "rect":
            self.resize_rect(self.canvas_pitch,self.rect_pitch,CANVAS_WIDTH/2,0,0,CANVAS_HEIGHT)
        elif inp == "help" or inp == "?":
            self.console.insert(END,"Here is an amazing help!%s"%(os.linesep))
        elif inp == "easteregg":
            self.console.insert(END,"You have found an easteregg! Congratulations!%s"%(os.linesep))
        elif inp == "exit" or inp == "bye":
            self.master.destroy()
        else:
            self.console.insert(END,"Unknown command %s. Maybe you should type help or ?.%s"%(inp,os.linesep))
    
    def resize_rect(self, can, item, x1, y1, x2, y2):
        #print("%d %d %d %d"%(x1,y1,x2,y2))
        can.coords(item, x1, y1, x2, y2)
        
    def update_controller(self):
        global lock_axis, axis
        lock_axis.acquire()
        # pitch = 0, thrust = 1
        self.resize_rect(self.canvas_pitch,self.rect_pitch,CANVAS_WIDTH/2,0,CANVAS_WIDTH/2+axis[0]*CANVAS_WIDTH/2,CANVAS_HEIGHT)
        self.resize_rect(self.canvas_thrust,self.rect_thrust,CANVAS_WIDTH/2,0,CANVAS_WIDTH/2+axis[1]*CANVAS_WIDTH/2,CANVAS_HEIGHT)
        lock_axis.release()
        
    def update_label(self):
        global lock_axis, axis
        lock_axis.acquire()
        s = "Pitch: %d %s Thrust: %d %s"%(axis[0]*CANVAS_WIDTH/2,os.linesep,axis[1]*CANVAS_WIDTH/2,os.linesep)
        lock_axis.release()
        self.status.config(text=s)
    
    

#
class thread_gui(threading.Thread):
    def __init__(self, root): 
        threading.Thread.__init__(self) 
        self.root = root
    
    def run(self):
        self.gui = gui(self.root)
        self.root.after(100,self.delay)
        self.root.mainloop()
    
    def delay(self):
        sleep(0.1)
        self.gui.update_controller()
        self.gui.update_label()
        self.root.after(100,self.delay)

class thread_controller(threading.Thread):
    def __init__(self,gp_root): 
        threading.Thread.__init__(self)
        self.gp = gp_root
    
    def run(self):
        global lock_end_intend, end_intend
        global lock_axis, axis
        while True:
            lock_end_intend.acquire()
            if end_intend:
                lock_end_intend.release()
                break
            lock_end_intend.release()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            lock_axis.acquire()
            for i in range(0,4):
                axis[i] = self.gp.get_axis(i)
            lock_axis.release()
            sleep(0.05)

if __name__ == '__main__':
    
    # Startup
    gui_root = Tk()
    t_gui = thread_gui(gui_root)
    threads.append(t_gui)
    t_gui.start()
    
    pygame.init()
    gp = pygame.joystick.Joystick(0)
    gp.init()
    
    t_controller = thread_controller(gp)
    threads.append(t_controller)
    t_controller.start()
    
    # Wait for threads to finish
    while True:
        if (not any([thread.isAlive() for thread in threads])):
            # All threads have stopped or user likes to end program
            break
        else:
            # Some threads are still going
            sleep(0.5)

    # Shutting down
