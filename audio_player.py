import os
import random
from PyQt6.QtCore import QObject, QTimer, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput


class AudioPlayer(QObject):
    def __init__(self, audio_path, parent = None):
        super().__init__(parent)

        
    