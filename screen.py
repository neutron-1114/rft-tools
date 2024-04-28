from pynput.keyboard import KeyCode
from pynput.mouse import Controller as MouseController
from PIL import Image
import mss

# 创建鼠标控制器实例
mouse = MouseController()


def capture_screen(left, top, width, height):
    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        img.show()


from pynput import keyboard


def on_press(key):
    if type(key) is KeyCode and key.char == '`':
        current_position = mouse.position
        left = int(current_position[0]) - 50
        top = int(current_position[1]) - 50
        width, height = 100, 100
        capture_screen(left, top, width, height)


with keyboard.Listener(
        on_press=on_press) as listener:
    listener.join()
