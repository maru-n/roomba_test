#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import struct
import sys

class RoombaController(object):
    """docstring for RoombaController"""
    def __init__(self, device_name):
        super(RoombaController, self).__init__()
        self.serial_manager = RoombaSerialManager(device_name)
        self.serial_manager.send_command('START')
        self.serial_manager.send_command('SAFE')

    def stop(self):
        self.drive(0, 0)

    def forward(self, velocity):
        self.drive(velocity, 0)

    def backward(self, velocity):
        self.drive(-velocity, 0)

    def spin_right(self, velocity):
        self.set_wheel_speed(-velocity, velocity)

    def spin_left(self, velocity):
        self.set_wheel_speed(velocity, -velocity)

    def set_wheel_speed(self, right_velocity, left_velocity):
        self.serial_manager.send_command('DRIVE_DIRECT', right_velocity, left_velocity)

    def fetch_battery(self):
        v = self.serial_manager.fetch_sensor_val("BATTERY_CARGE")
        return v

    def drive(self, velocity, radius):
        self.serial_manager.send_command('DRIVE', velocity, radius)

    def close(self):
        # TODO: implement speaker volume on hardware
        #self.serial_manager.send_command("RESET")
        self.serial_manager.close()
        self.serial_manager = None


class RoombaSerialManager(object):
    """docstring for RoombaSerialManager"""
    def __init__(self, device):
        super(RoombaSerialManager, self).__init__()
        self.device = device
        try:
            self.serial = serial.Serial(self.device, 115200, timeout=0.1)
        except:
            self.serial = None

    def write_code(self, code_list):
        if serial is None:
            Exception("serial device is not connected.")
        ret = self.serial.write(code_list)
        if ret != len(code_list):
            Exception("error occured on write serial code.")

    def send_command(self, command, *args):
        if command == 'START':
            self.write_code([128])
        elif command == 'RESET':
            self.write_code([7])
        elif command == 'STOP':
            self.write_code([173])
        elif command == 'SAFE':
            self.write_code([131])
        elif command == 'FULL':
            self.write_code([132])
        elif command == 'DIGIT_LEDS_ASCII':
            # TODO: Dummy data
            self.write_code([164, 65, 66, 67, 68])
        elif command == 'SEEK_DOCK':
            self.write_code([143])
        elif command == 'DRIVE':
            byte_cmd = struct.pack(">Bhh", 137, args[0], args[1])
            self.write_code(byte_cmd)
        elif command == 'DRIVE_DIRECT':
            byte_cmd = struct.pack(">Bhh", 145, args[0], args[1])
            self.write_code(byte_cmd)
        elif command == 'SENSORS':
            self.write_code([142, args[0]])
        else:
            Exception("Invalid command in send_command(): " + command)

    def read_bytes(self, num):
        bytes = self.serial.read(num)
        if len(bytes) != num:
            Exception("Couldn't read all serial datas.")
        return bytes

    def fetch_sensor_val(self, name):
        if name == 'BATTERY_CARGE':
            self.send_command('SENSORS', 25)
            ret_bytes = self.read_bytes(2)
            return int.from_bytes(ret_bytes, 'big')
        else:
            Exception("Invalid sensor name in get_sensor_val(): " + name)

    def close(self):
        self.serial.close()


def main():
    device = sys.argv[1]
    sm = RoombaSerialManager(device)

    for cmd in sys.argv[2:]:
        sm.send_command(cmd)


if __name__ == '__main__':
    main()
