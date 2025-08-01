import os
import random
from PyQt6.QtCore import QObject, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput, QMediaDevices, QAudioFormat


class AudioPlayer(QObject):
    def __init__(self, audio_path, audio_file, parent = None):
        super().__init__(parent)

        self.player = QMediaPlayer(self)
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)

        if audio_path == "RANDOM":
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