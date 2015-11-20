#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from roomba_serial_manager import RoombaSerialManager
import time
import struct
import sys


def main():
    if len(sys.argv) != 6:
        print("circle_run.py [serial device name] [radius (mm)] [duration (sec)] [angular rate (rad/sec)] [L/R]")
        return

    device = sys.argv[1]
    radius = float(sys.argv[2])
    duration = float(sys.argv[3])
    omg = float(sys.argv[4])
    orient = sys.argv[5]

    print("Device:", device)
    print("Radius:", radius, "mm")
    print("Duration", duration, "sec")
    print("Angular rate", omg)



    ROOMBA_DIA = 235
    rsm = RoombaSerialManager(device)

    rsm.send_command("START")
    rsm.send_command("FULL")
    time.sleep(1)
    start_time = time.time()
    vl = int(omg * (radius))
    vr = int(omg * (radius + ROOMBA_DIA))
    print(vl, vr)
    if orient == "L":
        byte_cmd = struct.pack(">Bhh", 145, vr, vl)
    elif orient == "R":
        byte_cmd = struct.pack(">Bhh", 145, vl, vr)
    else:
        return
    rsm.write_code(byte_cmd)

    while (time.time() - start_time) <= duration:
        sys.stdout.write("\r" + "%f"%(time.time()-start_time))

    rsm.send_command("DRIVE_DIRECT-STOP")
    rsm.send_command("RESET")


if __name__ == '__main__':
    main()
