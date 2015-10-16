#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import struct
import sys


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

    def send_command(self, command):
        DRIVE_SPEED = 200
        TURN_SPEED = 100

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
            self.write_code([164, 65, 66, 67, 68])
        elif command == 'SEEK_DOCK':
            self.write_code([143])
        # TODO: can I use byte() or to_bytes() on python 3?
        elif command == 'DRIVE_DIRECT-STOP':
            byte_cmd = struct.pack(">Bhh", 145, 0, 0)
            self.write_code(byte_cmd)
        elif command == 'DRIVE_DIRECT-FORWARD':
            byte_cmd = struct.pack(">Bhh", 145, DRIVE_SPEED, DRIVE_SPEED)
            self.write_code(byte_cmd)
        elif command == 'DRIVE_DIRECT-BACK':
            byte_cmd = struct.pack(">Bhh", 145, -DRIVE_SPEED, -DRIVE_SPEED)
            self.write_code(byte_cmd)
        elif command == 'DRIVE_DIRECT-TURN_RIGHT':
            byte_cmd = struct.pack(">Bhh", 145, -TURN_SPEED, TURN_SPEED)
            self.write_code(byte_cmd)
        elif command == 'DRIVE_DIRECT-TURN_LEFT':
            byte_cmd = struct.pack(">Bhh", 145, TURN_SPEED, -TURN_SPEED)
            self.write_code(byte_cmd)
        elif command == 'SENSORS':
            self.write_code([142])
        else:
            Exception("Invalid command in send_command(): " + command)

    def read_bytes(self, num):
        bytes = self.serial.read(num)
        if len(bytes) != num:
            Exception("Couldn't read all serial datas.")
        return bytes

    def get_sensor_val(self, command):
        self.send_command('SENSORS')
        if command == 'BATTERY_CARGE':
            self.write_code([25])
            ret_bytes = self.read_bytes(2)
            return int.from_bytes(ret_bytes, 'big')
        else:
            Exception("Invalid command in get_sensor_val(): " + command)


def main():
    device = sys.argv[1]
    sm = RoombaSerialManager(device)

    for cmd in sys.argv[2:]:
        sm.send_command(cmd)


if __name__ == '__main__':
    main()
