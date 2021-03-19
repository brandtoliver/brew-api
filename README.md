## brew-api
Reverse-engineering Nespresso Prodigios ble interface and creating flask api on Raspberry pi 4 (4gb).

Contributions are very welcome.

Running the solution:
1) Build docker image
2) Kill bluez on host machine: `sudo killall -9 bluetoothd` (see source 5)
3) Run docker container: `docker run --rm --net=host --privileged -it myimage:mytag`

## project status:
The api currently support `/status` (current status of nespresso machine e.g. "OK", "Brewing..." or "Slider error") and `/brew/<string:brew_type>` for brewing coffee.

### outstanding work:
* Add support for remaining machine alarms and status codes.
* Cleanup and commenting of code :)
* Use Class to handle machine state instead of dict.


## sources and inspiration:
1) Performing a reverse enigneering on a similar nespresso machine: https://gist.github.com/farminf/94f681eaca2760212f457ac59da99f23
2) Apples packetLogger tool for sniffing auth token from ble traffic: https://www.bluetooth.com/blog/a-new-way-to-debug-iosbluetooth-applications/
3) A Python module which allows communication with Bluetooth Low Energy devices: http://ianharvey.github.io/bluepy-doc/index.html
4) Project structure and code is heavly based on this EQ3 Bluetooth smart thermostats cli using bluepy: https://github.com/rytilahti/python-eq3bt
5) Running bluez and exposing hci to Docker container: https://stackoverflow.com/questions/28868393/accessing-bluetooth-dongle-from-inside-docker
6) Using ble on ubuntu (raspberry pi): https://raspberrypi.stackexchange.com/questions/114586/rpi-4b-bluetooth-unavailable-on-ubuntu-20-04 
