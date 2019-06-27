'''
mixers.py
Classes to wrap motor controllers into a functional drive unit.
'''

from __future__ import division

import math

import methods
from config import config


class BaseMixer():

    def update(self, throttle=0, angle=0):
        '''
        Update steering angle and throttle of vehicle
        '''
        pass


class AckermannSteeringMixer(BaseMixer):
    '''
    Mixer for vehicles steered by changing the
    angle of the front wheels.
    This is used for RC car-type vehicles.
    '''

    def __init__(self, steering_driver, throttle_driver):
        self.steering_driver = steering_driver # dirección
        self.throttle_driver = throttle_driver

    def update(self, throttle, angle):
        throttle = min(1, max(-1, -throttle)) # valor de la aceleración
        yaw = min(1, max(-1, methods.angle_to_yaw(angle))) # angulo de guiñada
        if not config.car.reverse_steering:
            yaw = -yaw
        self.throttle_driver.update(throttle)
        self.steering_driver.update(yaw)


class DifferentialSteeringMixer(BaseMixer):
    '''
    Mixer for vehicles using differential steering.
    This mixer emulates Ackermann steering on a differential steering
    rover.
    '''

    def __init__(self, left_driver, right_driver):
        self.left_driver = left_driver
        self.right_driver = right_driver

    def update(self, throttle, angle):
        throttle = min(1, max(-1, throttle))
        if abs(angle) < 1E-4:
            l_speed = throttle
            r_speed = throttle
        else:
            l_a = config.car.L
            w_d = config.car.W
            w_o = config.car.W_offset
            angle_radians = math.radians(angle)
            steer_tan = math.tan(angle_radians)
            r = l_a / steer_tan
            l_speed = throttle * (1.0 - (w_d * 0.5 - w_o)/r ) * \
                config.differential_car.left_mult
            r_speed = throttle * (1.0 + (w_d * 0.5 + w_o)/r ) * \
                config.differential_car.right_mult
        l_speed = min(max(l_speed, -1), 1)
        r_speed = min(max(r_speed, -1), 1)
        if config.car.reverse_steering:
            t_speed = l_speed
            l_speed = r_speed
            r_speed = t_speed
        if config.differential_car.left_reverse:
            l_speed = -l_speed
        if config.differential_car.right_reverse:
            r_speed = -r_speed
        self.left_driver.update(l_speed)
        self.right_driver.update(r_speed)
