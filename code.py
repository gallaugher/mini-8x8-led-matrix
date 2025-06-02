import time
import board
import busio
import adafruit_framebuf
from adafruit_ht16k33.matrix import Matrix8x8

# === Matrix Setup ===
i2c = busio.I2C(board.SCL, board.SDA)
matrix = Matrix8x8(i2c)
matrix.brightness = 1
matrix.fill(0)

# === Icons ===
smiley = [
    0b00111100,
    0b01000010,
    0b10100101,
    0b10000001,
    0b10100101,
    0b10011001,
    0b01000010,
    0b00111100,
]

lightbulb = [
    0b00111000,
    0b01000100,
    0b10000010,
    0b10000010,
    0b10000010,
    0b01000100,
    0b00111000,
    0b00010000,
]

heart = [
    0b00000000,
    0b01100110,
    0b11111111,
    0b11111111,
    0b11111111,
    0b01111110,
    0b00111100,
    0b00011000,
]

# === Message Text ===
text = " DIG IF YOU WILL THE HATCHERY! "

# === Buffer Prep ===
icon_width = 8
spacer = 2
padding = 8  # blank space before smiley for scroll-in
text_width = len(text) * 6  # 5px font + 1px spacing
end_icon_padding = 2  # space between text and heart

# Total buffer width
buffer_width = (
    padding + icon_width + spacer + text_width + end_icon_padding + icon_width + 8
)

# Create FrameBuffer
buf = bytearray(buffer_width)
fb = adafruit_framebuf.FrameBuffer(buf, buffer_width, 8, adafruit_framebuf.MVLSB)

# === Draw smiley icon ===
for y in range(8):
    row = heart[y]
    for x in range(8):
        if (row >> (7 - x)) & 0x01:
            fb.pixel(padding + x, y, 1)

# === Draw text ===
text_x = padding + icon_width + spacer
fb.text(text, text_x, 0, 1)

# === Draw heart at end ===
heart_x = text_x + text_width + end_icon_padding
for y in range(8):
    row = smiley[y]
    for x in range(8):
        if (row >> (7 - x)) & 0x01:
            fb.pixel(heart_x + x, y, 1)

# === Scroll Loop ===
while True:
    for offset in range(0, buffer_width - 8, 2):  # 2 pixels per step
        for x in range(8):
            col = buf[offset + x]
            for y in range(8):
                matrix[x, y] = 1 if (col & (1 << y)) else 0
        matrix.show()
        time.sleep(0.05)
