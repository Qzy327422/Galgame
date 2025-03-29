# music_manager.py
import os
import random
import pygame

class MusicController:
    def __init__(self):
        self.playlist = []
        self.current_index = 0
        self.config_file = os.path.join('settings', 'volume.ini')
        self.random_play = True
        self.volume = 0.5  
        
    
        self._load_initial_volume()
        self._load_music_files()

    def _load_initial_volume(self):
  
        try:
            if not os.path.exists('settings'):
                os.makedirs('settings')
            
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    self.volume = float(f.read().strip())
            else:
                self.save_volume()
        except Exception as e:
            print(f"加载音量配置失败: {str(e)}")
            self.volume = 0.5
            self.save_volume()

    def save_volume(self):

        try:
            with open(self.config_file, 'w') as f:
                f.write(str(round(self.volume, 2)))
        except Exception as e:
            print(f"保存音量失败: {str(e)}")

    def _load_music_files(self):
        music_dir = 'music'
        if os.path.exists(music_dir):
            self.playlist = [
                os.path.join(music_dir, f) 
                for f in os.listdir(music_dir)
                if f.lower().endswith(('.ogg', '.mp3', '.wav'))
            ]
            if self.random_play:
                random.shuffle(self.playlist)

    def start_playback(self):
        if not self.playlist:
            return
        
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=44100, size=-16, channels=2)
            
            pygame.mixer.music.load(self.playlist[self.current_index])
            pygame.mixer.music.set_volume(self.volume)
            pygame.mixer.music.play()
        except pygame.error as e:
            print(f"音乐加载失败: {str(e)}")

    def set_volume(self, volume):
        try:
            self.volume = max(0.0, min(1.0, volume))
            

            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=44100, size=-16, channels=2)
            
            pygame.mixer.music.set_volume(self.volume)
            self.save_volume()
        except Exception as e:
            print(f"设置音量失败: {str(e)}")



# 全局音乐控制器实例
music_controller = MusicController()