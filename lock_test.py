import time
import threading
run = True

def foo():
    while run:
        #print('.')
        time.sleep(0)
    print("not running")

def bar():
    time.sleep(2)
    run = False


t1 = threading.Thread(target=foo)
t1.start()
t2 = threading.Thread(target=bar)
t2.start()
while run:
    print(run)
    time.sleep(0.5)