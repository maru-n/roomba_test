#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from test01 import RoombaSerialManager
from threading import Timer
import sys
from getch import getch


roomba_serial_manager = None
update_sensor_timer = None


def update_sensor_state():
    global update_sensor_timer
    update_sensor_timer = Timer(0.5, update_sensor_state)
    update_sensor_timer.start()
    v = roomba_serial_manager.get_sensor_val("BATTERY_CARGE")
    sys.stdout.write("\r" + "battery: " + str(v))


def main():
    global roomba_serial_manager
    device = sys.argv[1]
    roomba_serial_manager = RoombaSerialManager(device)

    roomba_serial_manager.send_command("START")
    roomba_serial_manager.send_command("FULL")

    update_sensor_state()

    while True:

        c = getch()

        if c == 'q':
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
        elif c == 'c':
            roomba_serial_manager.send_command("SEEK_DOCK")

    roomba_serial_manager.send_command("RESET")


if __name__ == '__main__':
    main()
