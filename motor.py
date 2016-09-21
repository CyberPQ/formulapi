from threading import RLock

#lock to protect variable
lock = RLock()
#motor speed
leftspeed = .0
rightspeed = .0


def set_speed(left, right):
    with lock:
        leftspeed = left
        rightspeed = right

def add_speed(left, right):
    with lock:
        leftspeed += left
        rightspeed += right

def get_