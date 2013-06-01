from multiprocessing import Process

def foo(t):
    print("bla")

class bar():
    def __init__(self, name):
        print("hello")
    
    def run(self):
        print("run")
    


if __name__ == '__main__':
    b = bar("bob")
    p = Process(target=b.run, args=())
    p.start()
    p.join()