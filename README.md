# Circuitpython Scripts
examples and testing scripts for developing with circuitpython

## how to use
1. copy the file (clone the repo, download zip, copy the text, etc...)
2. with circuitpython board plugged in, place the .py file in CIRCUITPY drive (i.e. D:/CIRCUITPY)
3. to start automatically, rename (and overwrite) file to 'main.py'
4. to start manually, open REPL (Ctrl + c in serial monitor) and type: `import FILENAME.py`

### USB to UART script (UART bridge)
demonstrates how to turn the SAMD microcontroller running circuitpython into a USB-to-UART bridge via the REPL interface.
For example...
* using two USB cables, two Feather M0 boards, and some jumper wires

### TI ADS124S08 library for circuitpython
basic functions for the 24-bit ADC from TI: [http://www.ti.com/product/ADS124S08](http://www.ti.com/product/ADS124S08)
* see [xlab test board](https://github.com/maholli/XTB) for motivation/details
