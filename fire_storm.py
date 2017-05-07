import time
import animations
class FireStorm:
    def __init__(self,position,duration,damage):
        self.position = position
        self.duration = duration
        self.projectile_type = "FIRE"
        self.animations = animations.fire_storm_animation
        self.damage = damage
        self.damage_type = "MAGIC"
        self.rect = self.animations.get_animation("fire").get_current_frame(1).get_rect()
        self.rect.center = position.as_tuple()
        self.old_rect = self.rect.copy()
        self.t0 = time.time()
        self.isAlive = True
    def get_representation(self):
        t = time.time()
        return self.animations.get_animation("fire").get_current_frame(t - self.t0)
    def update(self):
        if not self.isAlive:
            print "why"
            self.isAlive = True
        if time.time() - self.t0 > self.duration:
            print time.time() - self.t0, self.duration,"fire"
            self.isAlive = False

class Explosion:
    def __init__(self,position,duration):
        self.position = position
        self.duration = duration
        self.projectile_type = "EXPLOSION"
        self.animations = animations.explosion_animation
        self.damage = 0
        self.damage_type = "NORMAL"
        self.rect = self.animations.get_animation("explosion").get_current_frame(1).get_rect()
        self.rect.center = position.as_tuple()
        self.old_rect = self.rect.copy()
        self.t0 = time.time()
        self.isAlive = True
        self.isFighting = False
    def get_representation(self):
        t = time.time()
        return self.animations.get_animation("explosion").get_current_frame(t - self.t0)
    def update(self,dummy):
        if time.time() - self.t0 > self.duration:
            self.isAlive = False