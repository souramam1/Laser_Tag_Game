import RPi.GPIO as io
import time

class receiver:

    PUSH_BUTTON_PIN = 18
    LIFE_LEDS = (27, 22, 23)
    RECEIVER_OUT = 10
    WAND_POWER = 4

    HIT_TIMEOUT = 0.02
    BUTTON_TIMEOUT = 3

    button_count: int
    button_time: float
    button_function: any
    hit_count: int
    hit_time: float
    hit_function: any

    life: int

    def __init__(self, button_func, hit_func):
        io.setmode(io.BCM)
        io.setwarnings(False)

        io.setup(self.PUSH_BUTTON_PIN, io.IN, pull_up_down=io.PUD_UP)
        io.setup(self.RECEIVER_OUT, io.IN, pull_up_down=io.PUD_UP)
        io.setup(self.LIFE_LEDS[0], io.OUT)
        io.setup(self.LIFE_LEDS[1], io.OUT)
        io.setup(self.LIFE_LEDS[2], io.OUT)
        io.setup(self.WAND_POWER, io.OUT)

        io.add_event_detect(self.PUSH_BUTTON_PIN, io.FALLING, 
        callback = self.button_pressed_callback)

        io.add_event_detect(self.RECEIVER_OUT, io.FALLING, 
        callback = self.signal_recieved_callback)

        self.button_function = button_func
        self.hit_function = hit_func
        
        self.button_count = 0
        self.button_time = time.time()

        self.hit_count = 0
        self.hit_time = time.time()

        self.life = 0

        self.set_life()

    def set_life(self):
        if self.life == 0:
            io.output(self.LIFE_LEDS[0], 0)
            io.output(self.LIFE_LEDS[1], 0)
            io.output(self.LIFE_LEDS[2], 0)
        elif self.life == 1:
            io.output(self.LIFE_LEDS[0], 0)
            io.output(self.LIFE_LEDS[1], 0)
            io.output(self.LIFE_LEDS[2], 1)
        elif self.life == 2:
            io.output(self.LIFE_LEDS[0], 0)
            io.output(self.LIFE_LEDS[1], 1)
            io.output(self.LIFE_LEDS[2], 1)
        elif self.life >= 3:
            io.output(self.LIFE_LEDS[0], 1)
            io.output(self.LIFE_LEDS[1], 1)
            io.output(self.LIFE_LEDS[2], 1)

    def activate_wand(self):
        io.output(self.WAND_POWER, 1)

    def disable_wand(self):
        io.output(self.WAND_POWER, 0)
    
    def reset_life(self):
        self.life = 3
        self.set_life()

    def decrease_life(self):
        self.life -= 1
        self.set_life()

    def button_pressed_callback(self, channel):
        print("Pressed!")
        if self.button_time + self.BUTTON_TIMEOUT <= time.time():
            self.button_count=0
            self.button_time = time.time()
        else:
            self.button_count+=1
            if self.button_count >= 3:
                self.button_function()
                self.button_count = 0
    
    def signal_recieved_callback(self, channel):
        #print(self.hit_count)
        if self.hit_time + self.HIT_TIMEOUT <= time.time():
            self.hit_count=0
            self.hit_time = time.time()
        else:
            self.hit_count+=1
            if self.hit_count >= 3:
                self.hit_function()
                self.hit_count = 0
