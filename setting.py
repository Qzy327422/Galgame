from tkinter import *
from threading import Thread
import os
from music_manager import music_controller

def update_volume(value):
    try:
        volume = float(value) / 100
        music_controller.set_volume(volume)
    except Exception as e:
        print(f"更新音量失败: {str(e)}")


def setting_1():
    print('按钮翻页')
    with open(os.path.join('settings', 'pages.ini'), 'w', encoding='utf-8') as path:
        path.write('1')


def setting_2():
    print('全屏点击翻页')
    with open(os.path.join('settings', 'pages.ini'), 'w', encoding='utf-8') as path:
        path.write('2')


def start_thread(func):
    thread = Thread(target=func)
    thread.start()

root = Tk()
Label(root, text="设置", font=("黑体", 20, "bold")).pack()
Label(root, text="重启后生效", font=("黑体", 10, "bold")).pack()
Label(root, text="WKの奇妙冒险-v0.4", font=("黑体", 7, "bold")).pack()
Label(root, text="by-qzy", font=("黑体", 7, "bold")).pack()
fr = LabelFrame(root, text="剧情翻页")
fr.pack(fill="both", padx=4)
Label(root, text="游戏音量调节").pack()
volume_scale = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=update_volume)
volume_scale.set(music_controller.volume * 100)  # 初始值
volume_scale.pack()

Button(fr, text="按钮翻页", command=lambda: start_thread(setting_1)).pack()
Button(fr, text="全屏点击翻页", command=lambda: start_thread(setting_2)).pack()

root.mainloop()