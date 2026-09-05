import time

count = 0

def decor(func):
    def wrapper():
        print("Wrapper -- start ....")
        func()
        print("Wrapper -- end ....")

    return wrapper

def timing(func):
    def wrapper():
        t = time.time()
        func()
        print(f"time executed: {(time.time() - t)}")
    return wrapper

@timing
@decor
def hello():
    global count
    count = count + 1
    print(f'Hello world. ({count})')


class CallCounter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kargs):
        self.count = self.count + 1
        self.func(*args, **kargs)
        print(f"Call {self.count} of {self.func.__name__!r}")

@CallCounter
def hello2():
    print("Hello world!")


class Repeat:
    def __init__(self, times=1):
        self.times = times

    def __call__(self, func):
        def wrapper(*args, **kargs):
            for _ in range(self.times):
                result = func(*args, **kargs)
            return result
        
        return wrapper

@Repeat(3)
def hello3():
    print('-- Hello world')

# timing(decor(hello))
hello()
print('-'*20)
hello2()
hello2()
print('-'*20)
hello3()
