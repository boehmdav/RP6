from tkinter import *

class App:
    def __init__(self, master):

        Button(master, text="QUIT", fg="red", command=master.quit).grid(row=1, column=0)
        Button(master, text="Hello", command=self.say_hi).grid(row=1, column=1)
        
        self.text = Text(master)
        self.text.grid(row=2, column=0, columnspan=2)
        self.text.bind("<KeyRelease>",self.on_key_press)
        self.canvas = Canvas(master, width=200, height=50)
        self.canvas.grid(row=0, column=0, columnspan=2)
        #x Pos1, y Pos1, x Pos2, y Pos2
        self.rect = self.canvas.create_rectangle(0, 0, 60, 75, fill="green")
        
    def resize_rect(self, item, x1, y1, x2, y2):
        self.canvas.coords(item, x1, y1, x2, y2)
        
    def say_hi(self):
        self.resize_rect(self.rect,0,0,100,100)
        print("hi there, everyone!")
        
    def on_key_press(self, event):
        if ord(event.char) == 13:
            print("Enter pressed")
            #print(self.text.get('1.0','1.end'))
            line, column = self.text.index('insert').split('.')
            print(self.text.get("%d.0"%(int(line)-1),"%d.end"%(int(line)-1)))
    

root = Tk()

app = App(root)

root.mainloop()