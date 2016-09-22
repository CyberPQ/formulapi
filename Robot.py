from threading import RLock


class Robot(object):
    #159mm
    ENTRAXE = 0.159

    def __init__(self):
        #lock to protect variable
        self.lock = RLock()
        #motor speed
        self.leftspeed = .0
        self.rightspeed = .0


    def set_speed(self, left, right):
        with self.lock:
            self.leftspeed = left
            self.rightspeed = right

    def add_speed(self, left, right):
        with self.lock:
            self.leftspeed += left
            self.rightspeed += right

    def get_deltarotation(self, dt):
        with self.lock:
            deltaleft = self.leftspeed * dt
            deltaright = self.rightspeed * dt
            d = (deltaleft + deltaright) / 2.
            if deltaright == deltaleft:
                return 0., d
            rayon = (self.ENTRAXE * d) / (deltaright - deltaleft)
            deltarotation = (deltaright - deltaleft)/(self.ENTRAXE)
            #deltarotation = d / rayon
        return deltarotation, d

    def get_absspeed(self):
        with self.lock:
            speed = (self.leftspeed + self.rightspeed) / 2.
            #print 'speed',self.leftspeed, self.rightspeed
        return speed

robot = Robot()