import pygame
import sys
import os
import math
import random
from backgrounds import load_backgrounds, load_images
import tkinter as tk
from tkinter import messagebox
import runpy
import threading
from tkinter import *
from music_manager import music_controller  # 新增音乐控制器导入

def my_function():
    runpy.run_path(os.path.join('setting.py'))

# 创建 Tkinter 窗口并设置为置顶
root = tk.Tk()
root.attributes('-topmost', 1)
root.withdraw()

# 初始化Pygame模块
pygame.init()
pygame.font.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2)  # 优化音频初始化

# 设置音乐结束事件
MUSIC_END_EVENT = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSIC_END_EVENT)

# 获取屏幕尺寸
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# 创建无边框窗口
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("Game")

# 加载背景资源
background_paths = load_backgrounds()
background_images = load_images(background_paths)
current_background = background_images['background1']
current_background_index = 0
show_extra_buttons = False


# 设置按钮颜色和位置大小
button_width = screen_width * 0.25
button_height = screen_height * 0.08
button_width2 = screen_width * 0.1
button_height2 = screen_height * 0.08

# 定义按钮的Y坐标
button_y1 = screen_height * 0.44
button_y2 = screen_height * 0.54
button_y3 = screen_height * 0.74
extra_button_y1 = screen_height * 0.93  # >>
extra_button_y2 = screen_height * 0.93  # exit
extra_button_y3 = screen_height * 0.93  # <<
extra_button_y4 = screen_height * 0.93  # save

button_color = (150, 255, 150)

# 计算按钮的X坐标，使其在屏幕中居中
button_x = screen_width * 0.2
button_x1 = screen_width * 0.97
button_x2 = screen_width * 0.4
button_x3 = screen_width * 0.045
button_x4 = screen_width * 0.6

# 定义按钮的Rect对象
button_rect1 = pygame.Rect(button_x - button_width / 2, button_y1, button_width, button_height)
button_rect2 = pygame.Rect(button_x - button_width / 2, button_y2, button_width, button_height)
button_rect3 = pygame.Rect(button_x - button_width / 2, button_y3, button_width, button_height)
extra_button_rect1 = pygame.Rect(button_x1 - button_width2 / 2, extra_button_y1, button_width2, button_height2)
extra_button_rect2 = pygame.Rect(button_x2 - button_width2 / 2, extra_button_y2, button_width2, button_height2)
extra_button_rect3 = pygame.Rect(button_x3 - button_width2 / 2, extra_button_y3, button_width2, button_height2)
extra_button_rect4 = pygame.Rect(button_x4 - button_width2 / 2, extra_button_y4, button_width2, button_height2)

# 新按钮的位置
new_button_y = screen_height * 0.64
new_button_rect = pygame.Rect(button_x - button_width / 2, new_button_y, button_width, button_height)

# 设置字体和文字大小
title_font_size = int(screen_height * 0.16)  # 转换为整数
title_font = pygame.font.Font('font/微软雅黑.ttf', title_font_size)  # 确保字体路径正确
title_text = title_font.render('WKの奇妙冒险', True, (255, 255, 255))
title_rect = title_text.get_rect(center=(screen_width // 3.3, screen_height * 0.2))

# 设置按钮文字大小
font_size = int(screen_height * 0.05)  # 转换为整数
font = pygame.font.Font('font/微软雅黑.ttf', font_size)  # 确保字体路径正确

# 初始化颜色变化的时间
color_change_interval = 20  # 颜色变化间隔20毫秒
last_color_time = pygame.time.get_ticks()

# 初始化是否绘制标题和按钮文字的标志变量
draw_title_text = True
draw_button_text = True

# 粒子效果
particles = []
particle_alpha_decay = 2
particle_lifespan = 10  # 粒子的生命周期，单位为帧

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # 使用饱和度较高的颜色
        self.color = (random.randint(160, 255), random.randint(160, 255), random.randint(160, 255))
        self.alpha = 255  # 初始透明度
        self.lifespan = particle_lifespan  # 设置生命周期

    def update(self, dt):
        self.alpha -= dt * particle_alpha_decay  # 更新透明度，使其逐渐消失
        if self.alpha < 0:
            self.alpha = 0
        self.lifespan -= 1
        if self.lifespan <= 0:
            return False
        return True

    def draw(self, screen):
        # 绘制粒子
        pygame.draw.circle(screen, (self.color[0], self.color[1], self.color[2], self.alpha), (int(self.x), int(self.y)), 3)

music_controller.start_playback()

# 主游戏循环
running = True
clock = pygame.time.Clock()
last_frame_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 处理音乐结束事件
        if event.type == MUSIC_END_EVENT:
            music_controller.next_track()

        # 检测鼠标按下事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            # 检查鼠标是否在按钮区域内
            if button_rect1.collidepoint(mouse_pos) and not show_extra_buttons:
                print("1")
                new = 1
                current_background_index = (current_background_index + 1) % 3
                current_background = list(background_images.values())[current_background_index]
                show_extra_buttons = True
                draw_title_text = False
                draw_button_text = False
            elif extra_button_rect1.collidepoint(mouse_pos) and show_extra_buttons:
                print(">>")
                if current_background_index < len(background_images) - 1:
                    new = new + 1
                    current_background_index += 1
                    current_background = list(background_images.values())[current_background_index]
            elif extra_button_rect2.collidepoint(mouse_pos) and show_extra_buttons:
                print("exit2")
                pygame.quit()
                sys.exit()

            elif extra_button_rect3.collidepoint(mouse_pos) and show_extra_buttons:
                print("<<")
                if new == 1:
                    print('背景2')
                    messagebox.showinfo('喵呜~', '已经是第一页啦')
                else:
                    new = new - 1
                    if current_background_index > 0:
                        current_background_index -= 1
                        current_background = list(background_images.values())[current_background_index]

            elif button_rect2.collidepoint(mouse_pos) and not show_extra_buttons:
                print("load")
                file_path = os.path.join('saves', 'save.ini')
                if os.path.exists(file_path):
                    with open(os.path.join('saves', 'save.ini'), 'r', encoding='utf-8') as loadduqu:
                        loadduqu2 = loadduqu.readline()
                        print(loadduqu2)
                        new = int(loadduqu2)
                        show_extra_buttons = True
                        draw_title_text = False
                        draw_button_text = False
                        current_background_index = new - 1
                        current_background_index += 1
                        current_background = list(background_images.values())[current_background_index]
                else:
                    print("无存档")
                    messagebox.showinfo('错误', '无存档')

            elif button_rect3.collidepoint(mouse_pos) and not show_extra_buttons:
                print("exit")
                pygame.quit()
                sys.exit()
            elif new_button_rect.collidepoint(mouse_pos) and not show_extra_buttons:
                print("setting")
                my_thread = threading.Thread(target=my_function)
                my_thread.start()


            elif extra_button_rect4.collidepoint(mouse_pos) and show_extra_buttons:
                print("save")
                with open(os.path.join('saves', 'save.ini'), 'w', encoding='utf-8') as path:
                    path.write(str(new))

        # 鼠标移动事件
        if event.type == pygame.MOUSEMOTION:
            for particle in particles:
                if not particle.update((pygame.time.get_ticks() - last_frame_time) / 1000):
                    particles.remove(particle)
            new_particle = Particle(event.pos[0], event.pos[1])
            particles.append(new_particle)
            last_frame_time = pygame.time.get_ticks()

    # 根据窗口大小调整背景图片大小
    screen.blit(pygame.transform.scale(current_background, (screen_width, screen_height)), (0, 0))

    # 绘制标题文字
    if draw_title_text:
        current_time = pygame.time.get_ticks()
        if current_time - last_color_time > color_change_interval:
            last_color_time = current_time
            hue = (current_time * 0.1) % 360
            color = [int(155 + 100 * math.sin(math.radians(hue + 360 * i / 3))) for i in range(3)]
            title_text = title_font.render('WKの奇妙冒险', True, (color[0], color[1], color[2]))
            title_text.set_alpha(170)
        screen.blit(title_text, title_rect)

    # 绘制按钮和按钮文字
    if not show_extra_buttons:
        pygame.draw.rect(screen, button_color, button_rect1, 4)
        pygame.draw.rect(screen, button_color, button_rect2, 4)
        pygame.draw.rect(screen, button_color, button_rect3, 4)
        pygame.draw.rect(screen, button_color, new_button_rect, 4)

        button_text1 = font.render('开始游戏', True, (0, 0, 0))
        button_text2 = font.render('读取存档', True, (0, 0, 0))
        button_text3 = font.render('退出', True, (0, 0, 0))
        new_button_text = font.render('设置', True, (0, 0, 0))

        text_rect1 = button_text1.get_rect(center=button_rect1.center)
        text_rect2 = button_text2.get_rect(center=button_rect2.center)
        text_rect3 = button_text3.get_rect(center=button_rect3.center)
        new_text_rect = new_button_text.get_rect(center=new_button_rect.center)

        screen.blit(button_text1, text_rect1)
        screen.blit(button_text2, text_rect2)
        screen.blit(button_text3, text_rect3)

        screen.blit(new_button_text, new_text_rect)
    else:
        pygame.draw.rect(screen, button_color, extra_button_rect1, -1)
        pygame.draw.rect(screen, button_color, extra_button_rect2, -1)
        pygame.draw.rect(screen, button_color, extra_button_rect3, -1)
        pygame.draw.rect(screen, button_color, extra_button_rect4, -1)

        extra_button_text1 = font.render('>>', True, (0, 0, 0))
        extra_button_text2 = font.render('退出', True, (0, 0, 0))
        extra_button_text3 = font.render('<<', True, (0, 0, 0))
        extra_button_text4 = font.render('保存', True, (0, 0, 0))

        extra_text_rect1 = extra_button_text1.get_rect(center=extra_button_rect1.center)
        extra_text_rect2 = extra_button_text2.get_rect(center=extra_button_rect2.center)
        extra_text_rect3 = extra_button_text3.get_rect(center=extra_button_rect3.center)
        extra_text_rect4 = extra_button_text4.get_rect(center=extra_button_rect4.center)

        screen.blit(extra_button_text1, extra_text_rect1)
        screen.blit(extra_button_text2, extra_text_rect2)
        screen.blit(extra_button_text3, extra_text_rect3)
        screen.blit(extra_button_text4, extra_text_rect4)

    # 绘制粒子
    for particle in particles:
        particle.draw(screen)

    pygame.display.flip()
    clock.tick(30)

pygame.mixer.music.stop()
pygame.quit()
