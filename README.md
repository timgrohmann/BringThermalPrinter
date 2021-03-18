# Bring! Thermal Printer

Lift your shopping experience to the next level.

## About

This is a python project to pretty print your shopping list from the "Bring!" app via a thermal printer.
It should be compatible with most ESC/POS 80mm Printers.

## Setup

You can install all the needed packages using `pip` and the included `requirements.txt`.

Create a `secret.py` file containing the following:

```py
USERNAME = 'youremail@address.com'
PASSWORD = 'The Password you login to Bring with'
LIST_NAME = 'The name of the list you want to print out'
```

Additionally, you may need to update the USB-Settings in `BringThermalPrinter.py`.

## Usage

To print directly via your thermal printer, execute `python BringThermalPrinter.py`.
If you want to see a preview, use `python BringThermalPrinter.py -file` to render the
output to a PNG-File.