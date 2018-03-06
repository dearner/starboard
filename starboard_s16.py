from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from time import sleep
import random
import colorsys

mode = 0
maxdrops = 500

options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 4
options.disable_hardware_pulsing = 0
options.gpio_slowdown = 1
options.brightness = 100
options.pwm_bits = 11
options.hardware_mapping="adafruit-hat"

mode = 0

class Drop:
    def __init__(self):
        global mode
        self.x = 0
        self.y = random.randint(0, 31)
        self.r = self.b = self.g = 0
        self.generateColor()
        self.speed = 1 + (random.random() * 4)
        self.strength = random.randint(40, 100)/100.0
    def generateColor(self):
        (r, g, b) = colorsys.hsv_to_rgb(random.random(), 1, 1)
        if (mode == 0):
            (r, g, b) = colorsys.hsv_to_rgb((self.y / 31.0), 1, 1)
        #mode == 2 leaves it at hsv
        self.r = int(r * 255)
        self.g = int(g * 255)
        self.b = int(b * 255)

        if (mode == 1):
            self.r = random.randint(0, 255)
            self.g = random.randint(0, 255)
            self.b = random.randint(0, 255)
        self.altr = int(r * 255)
        self.altg = int(g * 255)
        self.altb = int(b * 255)
        if (random.random() > .01 and mode == 3):
            self.r = self.g = self.b = random.randint(0, 255)
        
    def tick(self):
        self.erase()
        self.x += (self.speed / 2.0)
        if self.x > 127:
            self.x = 127
            self.strength = 0
        self.strength = self.strength * .977
        if (self.strength < 0):
            self.strength = 0
        self.draw()
    def draw(self):
        matrix.SetPixel(self.x, self.y, self.b*(self.strength), self.g*(self.strength), self.r*(self.strength))
        if (random.random() < .001):
            matrix.SetPixel(self.x, self.y, self.altb, self.altg, self.altr)

    def erase(self):
        matrix.SetPixel(self.x, self.y, 0, 0, 0)

matrix = RGBMatrix(options = options)
print ("Matrix initialized\n")


drops = []
for k in range (0, maxdrops):
    drops.append(Drop())

modeTicks = 1000
while (True):
    global mode, modeTicks
    for j in range(0, len(drops)):
        drops[j].tick()
        if drops[j].strength == 0:
           drops[j].erase()
           drops[j] = Drop()

    sleep(.01)
    modeTicks -= 1
    if modeTicks < 0:
        modeTicks = 10000
        mode += 1
        mode = mode % 4
