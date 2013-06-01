import threading

active_threads = []

##################################################
# 
##################################################
class PrimzahlThread(threading.Thread): 
    def __init__(self, zahl): 
        threading.Thread.__init__(self) 
        self.Zahl = zahl 
 
    def run(self): 
        i = 2 
        while i*i < self.Zahl: 
            if self.Zahl % i == 0: 
                print("%d ist nicht prim, da %d = %d * %d" % ( 
                    self.Zahl, self.Zahl, i, self.Zahl / i) )
                return 
            i += 1 
        print ("%d ist prim" % self.Zahl)
    
    

while True:
    _input = input("> ")
    if _input == "exit":
        break
    thread = PrimzahlThread(int(_input))
    active_threads.append(thread)
    thread.start()
    
for t in active_threads:
    if t.isAlive():
        t._stop()