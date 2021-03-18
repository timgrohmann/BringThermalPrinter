from PIL import Image, ImageDraw, ImageFont
import PIL.ImageOps
from datetime import datetime
import locale


class ImageGenerator():
    SML_SIZE = 20
    REG_SIZE = 25
    GRP_SIZE = 30
    RBT_FONT_SML = ImageFont.truetype('font/Roboto-Light.ttf', SML_SIZE)
    RBT_FONT_REG = ImageFont.truetype('font/Roboto-Regular.ttf', REG_SIZE)
    RBT_FONT_ITA = ImageFont.truetype('font/Roboto-BlackItalic.ttf', GRP_SIZE)
    RBT_FONT_HEA = ImageFont.truetype('font/Roboto-Black.ttf', GRP_SIZE)
    WIDTH = 576
    FORMAT = {
        'g': RBT_FONT_ITA,
        'i': RBT_FONT_REG,
    }

    def __init__(self):
        self.y = 0
        self.img = Image.new('L', (ImageGenerator.WIDTH, 10000), 255)
        self.d = ImageDraw.Draw(self.img)
        locale.setlocale(locale.LC_TIME, "de_DE")

    def generate_image(self, items: list):
        self.reset()
        self.print_header(items)

        for t, txt in items:
            font = ImageGenerator.FORMAT[t]

            if t == 'i':
                self.d.rectangle((ImageGenerator.WIDTH - 10 - ImageGenerator.REG_SIZE,
                                 self.y, ImageGenerator.WIDTH - 10, self.y + ImageGenerator.REG_SIZE))
                textln = font.getsize(txt)[0]
                self.d.line((20 + textln, self.y + ImageGenerator.REG_SIZE - 5, ImageGenerator.WIDTH -
                            20 - ImageGenerator.REG_SIZE, self.y + ImageGenerator.REG_SIZE - 5), fill=(128))
            if t == 'g':
                try:
                    group_line_image = Image.open(f'img/{txt}.png', 'r')
                    group_line_image = group_line_image.convert('L')
                    group_line_image = PIL.ImageOps.pad(group_line_image, (int(
                        ImageGenerator.GRP_SIZE * 1.5), int(ImageGenerator.GRP_SIZE * 1.5)))
                    group_line_image = PIL.ImageOps.invert(group_line_image)

                    self.img.paste(group_line_image, (int(
                        ImageGenerator.WIDTH - ImageGenerator.GRP_SIZE * 1.6), self.y + 10))
                except:
                    pass
                self.y += 20

            self.print_text_line(txt, font)

        new_height = int(self.y)
        self.img = self.img.resize((ImageGenerator.WIDTH, new_height), box=(
            0, 0, ImageGenerator.WIDTH, new_height))

        return self.img

    def reset(self):
        self.y = 0
        self.img.paste(255, [0, 0, self.img.size[0], self.img.size[1]])

    def print_header(self, items: list):
        header_image = Image.open(f'img/t.png', 'r')
        header_image = header_image.convert('L')
        header_image = PIL.ImageOps.pad(header_image, (150, 150), color=255)
        self.img.paste(header_image, (100, 0))
        self.d.text((250, 30), f"tims", font=ImageGenerator.RBT_FONT_HEA)
        self.d.text((250, 60), f"tolle", font=ImageGenerator.RBT_FONT_HEA)
        self.d.text((250, 90), f"shoppinglist",
                    font=ImageGenerator.RBT_FONT_HEA)
        self.y += 150

        date = datetime.now().strftime("%A, %d. %B %Y")
        count = sum(1 for x in items if x[0] == 'i')
        self.print_text_line(
            f"Einkauf am {date}", font=ImageGenerator.RBT_FONT_SML, center=True)
        self.print_text_line(
            f"Insgesamt {count} Artikel", font=ImageGenerator.RBT_FONT_SML, center=True)

    def print_text_line(self, text: str, font: ImageFont.ImageFont, center: bool = False):
        x = 10 if not center else ImageGenerator.WIDTH/2
        anchor = "ma" if center else "la"
        self.d.text((x, self.y), text, font=font, anchor=anchor)
        self.y += int(font.size * 1.3)


if __name__ == "__main__":
    gen = ImageGenerator()
    image = gen.generate_image(formatting.printable_items())
    image.save("list_to_print.png")
