# brew-api
Reverse engineering nespresso prodigios ble interface and creating flask api on raspberry pi.


## Sources and inspiration:
1) Performing a reverse enigneering on a similar nespresso machine: https://gist.github.com/farminf/94f681eaca2760212f457ac59da99f23
2) Apples packetLogger tool for sniffing auth token from ble traffic: https://www.bluetooth.com/blog/a-new-way-to-debug-iosbluetooth-applications/
3) A Python module which allows communication with Bluetooth Low Energy devices: http://ianharvey.github.io/bluepy-doc/index.html
4) Project structure and code is heavly based on this EQ3 Bluetooth smart thermostats cli using bluepy: https://github.com/rytilahti/python-eq3bt
