#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from roomba_serial_manager import RoombaController
from threading import Timer
import sys
from getch import getch
import subprocess


roomba_controller = None
update_sensor_timer = None

DRIVE_SPEED = 200
SPIN_SPEED = 100


def update_sensor_state():
    global roomba_controller
    v = roomba_controller.get_battery()
    sys.stdout.write("\r" + "battery: " + str(v))
    global update_sensor_timer
    update_sensor_timer = Timer(0.5, update_sensor_state)
    update_sensor_timer.start()


def print_command_usage():
    print("w: forward | s: back | d: right | a: left | SPACE: stop | ESC: quit")


def main():
    if len(sys.argv) != 2:
        print("need serial device name.")
        return


    device = sys.argv[1]
    lsof = subprocess.Popen(['lsof', device], stdout=subprocess.DEVNULL).wait()
    if lsof == 0:
        print("\033[31mError: \033[39m devide %s is used by other process." % device)
        exit()

    global roomba_controller
    roomba_controller = RoombaController(device)


    print_command_usage()
    update_sensor_state()

    while True:
        c = getch()
        if c == '\x1b':
            global update_sensor_timer
            update_sensor_timer.cancel()
            print("")
            break
        elif c == "w":
            roomba_controller.forward(DRIVE_SPEED)
        elif c == "s":
            roomba_controller.backward(DRIVE_SPEED)
        elif c == "d":
            roomba_controller.spin_right(SPIN_SPEED)
        elif c == "a":
            roomba_controller.spin_left(SPIN_SPEED)
        elif c == ' ':
            roomba_controller.stop()

    roomba_controller.close()


if __name__ == '__main__':
    main()
