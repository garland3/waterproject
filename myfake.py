# import fake_rpi
# fake_rpi.py
class Base_GPIO:
    def __init__(self):
        self.pin_states = {}

    def setmode(self, mode):
        print(f"Fake RPi: Set mode to {mode}")

    def setup(self, pin, mode):
        print(f"Fake RPi: Setup pin {pin} as {mode}")
        self.pin_states[pin] = False

    def output(self, pin, state):
        print(f"Fake RPi: Set pin {pin} to {state}")
        self.pin_states[pin] = state

    def cleanup(self):
        print("Fake RPi: Cleaning up")
        self.pin_states = {}
        
    BCM = "BCM"
    OUT = "OUT"
    HIGH = 1
    LOW = 0
GPIO = Base_GPIO()