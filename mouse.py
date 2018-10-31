from adafruit_circuitplayground.express import cpx
from adafruit_hid.mouse import Mouse
import board

while True:
    if cpx.switch:
        cpx.red_led = False
        if cpx.touch_A4:
            Mouse().move(-1, 0, 0)
        if cpx.touch_A3:
            Mouse().move(1, 0, 0)
        if cpx.touch_A7:
            Mouse().move(0, -1, 0)
        if cpx.touch_A1:
            Mouse().move(0, 1, 0)
        if cpx.button_a:
            Mouse().press(Mouse.LEFT_BUTTON)
            while cpx.button_a:    # Wait for button A to be released
                pass
            m.release(Mouse.LEFT_BUTTON)
        if cpx.button_b:
            m.press(Mouse.RIGHT_BUTTON)
            while cpx.button_b:    # Wait for button B to be released
                pass
            Mouse().release(Mouse.RIGHT_BUTTON)
    else:
        cpx.red_led = True
        x, y, z = cpx.acceleration
        x_int = int(x)
        y_int = int(y)
        z_int = int(z)
        Mouse().move(x_int, y_int)
        if cpx.button_a:
            Mouse().press(Mouse.LEFT_BUTTON)
            while cpx.button_a:    # Wait for button A to be released
                pass
            Mouse().release(Mouse.LEFT_BUTTON)
        if cpx.button_b:
            Mouse().press(Mouse.RIGHT_BUTTON)
            while cpx.button_b:    # Wait for button B to be released
                pass
            Mouse().release(Mouse.RIGHT_BUTTON)
    
    