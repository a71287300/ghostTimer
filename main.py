import re
import threading
import keyboard
import pygame
import time
import configparser
import tkinter as tk

config = configparser.ConfigParser()
config.read('config.ini')
pygame.init()

# 加载音乐文件
pygame.mixer.music.load("./ghostAlert.mp3")  # 替换为你的音乐文件路径

initial_interval = int(config.get('Time', 'initial_interval'))
loop_interval = int(config.get('Time', 'loop_interval'))
# 监听键盘事件
playing = False  # 用于标记是否正在播放音乐
end_pressed = False  # 用于标记是否按下End键
play_interval = initial_interval
start_time = None  # 用于记录开始播放音乐的时间

def rgb_to_hex(rgb_str):
    # 使用正则表达式提取RGB值
    rgb_match = re.match(r"rgb\((\d+),(\d+),(\d+)\)", rgb_str)
    
    if rgb_match:
        r, g, b = map(int, rgb_match.groups())
        hex_color = "#{:02x}{:02x}{:02x}".format(r, g, b)
        return hex_color
    else:
        return None
    
    
class FloatingWindow:
    def __init__(self, root):
        
        font_size = int(config.get('Display', 'font_size'))
        font_color_rgb = config.get('Display', 'font_color')
        font_background_rgb = config.get('Display', 'font_background')
        initial_X = config.get('Display', 'initial_X')
        initial_Y = config.get('Display', 'initial_Y')
        xy = initial_X+'+'+initial_Y
        wh = str(font_size*9) + "x" + str(font_size*2)
        self.root = root
        self.root.title("Timer")
        self.root.overrideredirect(True)
        if display:
            alpha = 0.7
        else:
            alpha = 0
        self.root.wm_attributes('-alpha', alpha)
        self.root.geometry(wh+"+"+xy)
        self.root.attributes('-topmost', True)
        self.label = tk.Label(root, text="等待啟動", font=("Arial", font_size), bg=rgb_to_hex(font_background_rgb), fg=rgb_to_hex(font_color_rgb))
        self.label.pack(fill="both", expand=True)
       
        
    
    def change_text(self, new_text):
        self.label.config(text=new_text)

def stop_music():
    global playing, end_pressed, play_interval
    if playing:
        # 如果正在播放音乐，停止播放音乐
        pygame.mixer.music.stop()
        playing = False
        end_pressed = True
        play_interval = initial_interval
        if display:
            window.change_text("暫停播放")
        time.sleep(0.1)
        end_pressed = False

def play_music():
    global playing, play_interval, start_time
    while not end_pressed: 
        
        if not playing:
            # 如果没有正在播放，开始播放音乐
            pygame.mixer.music.play()
            playing = True
            start_time = time.time()
        elif time.time() - start_time >= play_interval:
            # 如果已经播放了一次音乐并且时间间隔达到指定值，再次播放音乐 
            pygame.mixer.music.play()
            if play_interval == initial_interval:
                play_interval = loop_interval  # 设置下一次播放的时间间隔为10秒
            start_time = time.time()

        # 打印当前等待时间
        remaining_time = play_interval - (time.time() - start_time)
        newtext = "剩餘時間:" + str(int(remaining_time)) +"秒" 
        if display:
            if remaining_time < 1 or remaining_time > play_interval-2.5:
                window.change_text("鬼來了!!")
            else:
                window.change_text(newtext)
        time.sleep(0.1)

def exit_app():
    if display:
        window.change_text("關閉中...")
    else:
        print("關閉中...")
    root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    display = config.getboolean('Display', 'enable')
    window = FloatingWindow(root)
    start_key = config.get('Hotkey', 'start_key')
    stop_key = config.get('Hotkey', 'stop_key')
    quit_key = config.get('Hotkey', 'quit_key')
    keyboard.on_press_key(start_key, lambda e: threading.Thread(target=play_music).start())
    keyboard.on_press_key(stop_key, lambda e: stop_music())
    keyboard.add_hotkey(quit_key, exit_app)
    root.mainloop()
