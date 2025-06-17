# led_modes_async.py (Fix: Breathing Mode Thruster + Reset Thruster Color + Speed Boost)
import asyncio
import math
import board
import busio
import random
from adafruit_pca9685 import PCA9685

# Setup I2C and PCA9685
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x40)
pca.frequency = 1500  # Slight boost for smoother PWM

# LED channel map
leds = {
    "head": 0,
    "chest": 1,
    "shoulderL": 2,
    "shoulderR": 3,
    "kneeL": 4,
    "kneeR": 5,
    "thrusterR": 6,
    "thrusterG": 7,
    "thrusterB": 8
}

# Twinkle LED state
static_leds = ["head", "chest", "shoulderL", "shoulderR", "kneeL", "kneeR"]

# Mode state
active_task = None
thruster_task = None
thruster_color_mode = 0
last_color_change = asyncio.get_event_loop().time()
color_duration = 5.0
current_mode_name = "startup"

# PWM helpers
def set_pwm(name, value):
    try:
        value = max(0, min(255, value))
        pca.channels[leds[name]].duty_cycle = int((255 - value) / 255 * 65535)
    except OSError as e:
        print(f"I2C error in set_pwm({name}): {e}")
        raise e

def set_rgb(r, g, b):
    set_pwm("thrusterR", r)
    set_pwm("thrusterG", g)
    set_pwm("thrusterB", b)

# Thruster sequence task
async def thruster_runner():
    global thruster_color_mode, last_color_change
    while True:
        now = asyncio.get_event_loop().time()
        if now - last_color_change > color_duration:
            thruster_color_mode = (thruster_color_mode + 1) % 3
            last_color_change = now

        if thruster_color_mode == 0:
            await pulse_color(0, 0, 255)
        elif thruster_color_mode == 1:
            await pulse_color(255, 0, 0)
        else:
            await pulse_flame_mix()

# Color effects
async def pulse_color(r, g, b):
    for i in range(0, 256, 10):  # faster sweep
        scale = i / 255
        set_rgb(int(r * scale), int(g * scale), int(b * scale))
        await asyncio.sleep(0.0015)
    for i in range(255, 100, -10):
        scale = i / 255
        set_rgb(int(r * scale), int(g * scale), int(b * scale))
        await asyncio.sleep(0.0015)

async def pulse_flame_mix():
    for i in range(0, 256, 10):
        r = 255
        g = random.randint(100, 180)
        b = random.randint(0, 50)
        scale = i / 255
        set_rgb(int(r * scale), int(g * scale), int(b * scale))
        await asyncio.sleep(0.002)
    for i in range(255, 100, -10):
        r = 255
        g = random.randint(100, 180)
        b = random.randint(0, 50)
        scale = i / 255
        set_rgb(int(r * scale), int(g * scale), int(b * scale))
        await asyncio.sleep(0.002)

# LED Modes (unchanged except for shared thruster sequences)
async def mode_static():
    global current_mode_name
    current_mode_name = "static"
    for name in static_leds:
        set_pwm(name, 200)
    set_rgb(0, 0, 255)
    while True:
        await asyncio.sleep(1)

async def mode_breathe():
    global current_mode_name, thruster_color_mode, last_color_change
    current_mode_name = "breathe"
    angles = {name: random.randint(0, 360) for name in static_leds}
    thruster_last_change = asyncio.get_event_loop().time()
    while True:
        for name in static_leds:
            angle = angles[name]
            brightness = int((math.sin(math.radians(angle)) + 1) * 127.5)
            set_pwm(name, brightness)
            angles[name] = (angle + 3) % 360

        now = asyncio.get_event_loop().time()
        if now - thruster_last_change > color_duration:
            thruster_color_mode = (thruster_color_mode + 1) % 3
            thruster_last_change = now

        if thruster_color_mode == 0:
            await pulse_color(0, 0, 255)
        elif thruster_color_mode == 1:
            await pulse_color(255, 0, 0)
        else:
            await pulse_flame_mix()

        await asyncio.sleep(0.02)

async def mode_flicker():
    global current_mode_name, thruster_color_mode, last_color_change
    current_mode_name = "flicker"
    while True:
        for name in static_leds:
            set_pwm(name, random.randint(50, 200))
        await asyncio.sleep(0.05)

        now = asyncio.get_event_loop().time()
        if now - last_color_change > color_duration:
            thruster_color_mode = (thruster_color_mode + 1) % 3
            last_color_change = now

        if thruster_color_mode == 0:
            await pulse_color(0, 0, 255)
        elif thruster_color_mode == 1:
            await pulse_color(255, 0, 0)
        else:
            await pulse_flame_mix()

async def mode_startup():
    global current_mode_name
    current_mode_name = "startup"
    async def fade(name, delay, idx):
        await asyncio.sleep(delay)
        for i in range(0, 256, 5):
            set_pwm(name, i)
            await asyncio.sleep(0.01)
        for i in range(255, -1, -5):
            set_pwm(name, i)
            await asyncio.sleep(0.01)

    tasks = [asyncio.create_task(fade(name, idx * 0.015, idx)) for idx, name in enumerate(leds)]
    await asyncio.gather(*tasks)

# Controller
async def run_mode(mode_fn):
    global active_task
    if active_task:
        active_task.cancel()
        try:
            await active_task
        except asyncio.CancelledError:
            pass
    active_task = asyncio.create_task(mode_fn())

# Startup
async def main():
    global thruster_task
    thruster_task = asyncio.create_task(thruster_runner())
    await run_mode(mode_startup)

loop = asyncio.get_event_loop()
loop.create_task(main())
