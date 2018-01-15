#!/usr/bin/python

# script to drive the individual soccer bots 
# Author: Yun Chang 

from __future__ import division
import time

# Import the PCA9685 module for servo driver 
import Adafruit_PCA9685
import numpy as np 

import sys
import socket
import select

# Initialise the PCA9685 using the default address (0x40) i2c
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure servo pulse lengths for rotating speed 
stationary = 375 # corresponds to 90 degrees: stationary 
max_pulse = 600 # Max pulse length out of 4096
min_pulse = 150 # Min pulse length out of 4096
right_forward = 1
right_reverse = -1
left_forward = 1
left_reverse = -1 

# physical constants 
max_speed = 2. # max 2 m/s
max_angv = np.pi # max pi rad/s 

right_channel = 0
left_channel = 1

# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    pulse_length //= 4096     # 12 bits of resolution
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)


def drive(speed, ang_vel):
    # let's say the max is 2m/s 
    # set forward first 
    right_pulse = speed/max_speed*(max_pulse - stationary)*right_forward + stationary
    left_pulse = speed/max_speed*(max_pulse - stationary)*left_forward + stationary
    # positive ang_vel: turn left 
    # negative ang_vel: turn right 
    pulse_diff = (max_pulse - stationary)*ang_vel/max_angv
    if pulse_diff > 0:
        left_pulse -= pulse_diff
    else:
        right_pulse += pulse_diff
    pwm.set_pwm(right_channel, 0, right_pulse)
    pwm.set_pwm(left_channel, 0, left_pulse)

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if len(sys.argv) != 3:
        print("Correct usage: script, IP address, port number")
        exit()
    IP_address = str(sys.argv[1])
    Port = int(sys.argv[2])
    server.connect((IP_address, Port))

    while True:
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]

        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
     
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                command = message.split()
                cmd_spd = float(command[0])
                cmd_angv = float(command[1])
            # else:
            #     message = sys.stdin.readline()
            #     server.send(message.encode('utf-8'))
            #     sys.stdout.write("<You> ")
            #     sys.stdout.write(message)
            #     sys.stdout.flush()
    server.close()