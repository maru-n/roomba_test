#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test01 import RoombaSerialManager
from threading import Timer
import sys
from getch import getch
import subprocess


roomba_serial_manager = None
update_sensor_timer = None


def update_sensor_state():
    global update_sensor_timer
    update_sensor_timer = Timer(0.5, update_sensor_state)
    update_sensor_timer.start()
    v = roomba_serial_manager.get_sensor_val("BATTERY_CARGE")
    sys.stdout.write("\r" + "battery: " + str(v))


def print_command_usage():
    print("w: forward | s: back | d: right | a: left | SPACE: stop | ESC: quit")

def main():
    if len(sys.argv) != 2:
        print("need serial device name.")
        return

    global roomba_serial_manager
    device = sys.argv[1]
    lsof = subprocess.Popen(['lsof', device], stdout=subprocess.DEVNULL).wait()
    if lsof == 0:
        print("\033[31mError: \033[39m devide %s is used by other process." % device)
        exit()

    roomba_serial_manager = RoombaSerialManager(device)

    roomba_serial_manager.send_command("START")
    roomba_serial_manager.send_command("FULL")

    print_command_usage()
    update_sensor_state()
    while True:

        c = getch()

        if c == '\x1b':
            update_sensor_timer.cancel()
            print("")
            break
        elif c == "w":
            roomba_serial_manager.send_command("DRIVE_DIRECT-FORWARD")
        elif c == "s":
            roomba_serial_manager.send_command("DRIVE_DIRECT-BACK")
        elif c == "d":
            roomba_serial_manager.send_command("DRIVE_DIRECT-TURN_RIGHT")
        elif c == "a":
            roomba_serial_manager.send_command("DRIVE_DIRECT-TURN_LEFT")
        elif c == ' ':
            roomba_serial_manager.send_command("DRIVE_DIRECT-STOP")

    roomba_serial_manager.send_command("RESET")


if __name__ == '__main__':
    main()
