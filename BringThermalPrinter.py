from escpos.printer import Usb

from BringAPI import BringAPI
from ListFormatter import ListFormatter
from ImageGenerator import ImageGenerator

import sys
import secret


class BringThermalPrinter():
    def __init__(self, username, password):
        self.api = BringAPI(username, password)
        self.formatter = ListFormatter(
            self.api.get_articles_locale(), self.api.get_catalog_locale())
        self.generator = ImageGenerator()

    def generate_image(self, listname):
        list_content = self.api.get_list(listname)
        list_details = self.api.get_list_details(listname)

        formatted_list = self.formatter.printable_items(
            list_content, list_details)

        return self.generator.generate_image(formatted_list)

    def print_to_file(self, listname):
        self.generate_image(listname).save("list_to_print.png")

    def print(self, listname):
        p = Usb(0x0483, 0x5743)
        p.image(self.generate_image(listname))
        p.cut()


if __name__ == "__main__":
    BTP = BringThermalPrinter(secret.USERNAME, secret.PASSWORD)

    args = sys.argv
    if "-file" in args:
        BTP.print_to_file(secret.LIST_NAME)
    else:
        BTP.print(secret.LIST_NAME)
