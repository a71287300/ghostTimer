import threading
import keyboard
import pygame
import time
import sys
import configparser
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

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

class FloatingWindow(QWidget):
    def __init__(self):
        super().__init__()
        if display:
            print("Display mode", display)
            self.setWindowTitle("Timer")
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
            x = int(config.get('Display', 'initial_X'))
            y = int(config.get('Display', 'initial_Y'))
            self.setGeometry(0, 0, x+2560, y+1440)
            # 创建文本标签并设置文本、字体、颜色和背景色（带透明度）
            self.label = QLabel("等待啟動", self)
            font_size = int(config.get('Display', 'font_size'))
            self.label.setGeometry(x, y, x+font_size*7, y+font_size*2)
            # 设置字体和颜色
            font = QFont()
            
            font.setPointSize(font_size)
            self.label.setFont(font)
            # 设置红色文本和白色背景，背景颜色带透明度（50%）
            font_color = config.get('Display', 'font_color')
            font_background = config.get('Display', 'font_background')
            font_setting = "color: " + font_color + "; background-color: " + font_background + ";"
            self.label.setStyleSheet(font_setting)
            self.show()
    
    def change_text(self, new_text):
        # 这个函数会在按钮被点击时调用，用于更改文本内容
        self.label.setText(new_text)

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
    app.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    global display 
    display = config.getboolean('Display', 'enable')
    if display:
        window = FloatingWindow()
    start_key = config.get('Hotkey', 'start_key')
    stop_key = config.get('Hotkey', 'stop_key')
    quit_key = config.get('Hotkey', 'quit_key')
    keyboard.on_press_key(start_key, lambda e: threading.Thread(target=play_music).start())
    keyboard.on_press_key(stop_key, lambda e: stop_music())
    keyboard.add_hotkey(quit_key, exit_app)
    sys.exit(app.exec_())