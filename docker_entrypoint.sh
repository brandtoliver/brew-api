#!/bin/bash

echo 'starting ble service'
service dbus start
bluetoothd &


echo 'running api.py'
python src/api.py
