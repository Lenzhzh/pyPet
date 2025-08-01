import os
import random
import pygame
from PyQt6.QtCore import QObject, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices, QAudioFormat


class AudioPlayer(QObject):
    '''
    抽象父类，声音播放器。
    '''
    def __init__(self, audio_path, audio_file, parent = None):
        super().__init__(parent)

        if audio_file == "RANDOM":
            self.audio_files = self._find_audio_files()
        else :
            self.audio_files = [audio_file]
        
        self._fix_file_path(audio_path)

    def _find_audio_files(self):
        try:
            return [f for f in os.listdir(self.audio_folder) if f.endswith(('.mp3', '.wav', '.ogg'))]
        except FileNotFoundError:
            return []
    
    def _fix_file_path(self, path):
        audio_files = []
        for f in self.audio_files:
            f_path = os.path.join(path, f)
            audio_files.append(f_path)
        self.audio_files = audio_files

    def play_random_sound(self):
        chosen_file = random.choice(self.audio_files)
        source = QUrl.fromLocalFile(chosen_file)

        self.player.setSource(source)
        self.player.play()
    
    def start(self):
        if self.audio_files:
            self.play_random_sound()
        
    def stop(self):
        self.player.stop()


class AudioPlayerWithPyqt6(AudioPlayer):
    '''
    不知道为什么我用不了。其实这个才是本来的选项。
    '''
    def __init__(self, audio_path, audio_file, parent=None):
        super().__init__(audio_path, audio_file, parent)
        self.init_QtMultimedia()

    def init_QtMultimedia(self):
        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

    def play_random_sound(self):
        chosen_file = random.choice(self.audio_files)
        source = QUrl.fromLocalFile(chosen_file)

        self.player.setSource(source)
        self.player.play()

    def stop(self):
        self.player.stop()


class AudioPlayerWithPygame(AudioPlayer):
    '''
    使用pygame进行发声。
    '''
    def __init__(self, audio_path, audio_file, parent=None):
        super().__init__(audio_path, audio_file, parent)
        pygame.mixer.init()

    def stop(self):
        pygame.mixer.music.stop()

    def play_random_sound(self):
        if pygame.mixer.get_busy():
            return
        
        chosen_file = random.choice(self.audio_files)

        pygame.mixer.music.load(chosen_file)
        pygame.mixer.music.play()
    
            
        