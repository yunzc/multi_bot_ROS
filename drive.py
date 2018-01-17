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


vehicle_id = '2'
vehicle_r = 0.0475 # (m) vehicle radius 
# Initialise the PCA9685 using the default address (0x40) i2c
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

# Configure servo pulse lengths for rotating speed 
r_stationary = 391 # corresponds to 90 degrees: stationary 
l_stationary = 390
max_pulse = 600 # Max pulse length out of 4096
min_pulse = 150 # Min pulse length out of 4096
right_forward = -1
right_reverse = 1
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


def drive(forward_vel, ang_vel):
    # let's say the max is 2m/s
    # first find desired vel for wach wheel 
    right_vel = forward_vel + ang_vel*vehicle_r
    left_vel = forward_vel - ang_vel*vehicle_r
    # set pulse
    right_pulse = int(right_vel/max_speed*(max_pulse - r_stationary)*right_forward + r_stationary)
    left_pulse = int(left_vel/max_speed*(max_pulse - l_stationary)*left_forward + l_stationary)
    # positive ang_vel: turn left 
    # negative ang_vel: turn right 
    print(right_pulse, left_pulse)
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

    # drive(1, 0.5)
    connected = False
    while not connected:
        server.send(vehicle_id.encode('utf-8'))
        message = server.recv(2048)
        if message == "Connected to server":
            connected = True
            
    print("connected")

    while True:
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, server]

        read_sockets, write_socket, error_socket = select.select(sockets_list,[],[])
        
        print("listening and executing")
        
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                command = message.split()
                cmd_spd = float(command[0])
                cmd_angv = float(command[1])
                drive(cmd_spd, cmd_angv)
    print("Disconnecting...")
    server.close()