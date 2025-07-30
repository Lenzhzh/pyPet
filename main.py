import sys
import os
import random
import time
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QMovie, QMouseEvent, QPixmap, QIcon, QAction, QVector2D
from PyQt6.QtCore import Qt, QPoint, QTimer, QSize, QEvent

from state import PetState



class Deskpet(QWidget):

    def __init__(self):
        super().__init__()
        self.isDebug = True
        self.resource_path = './resource/img/'

        self.movies = {
            state: QMovie(os.path.join(self.resource_path, f"{state.value}.gif"))
            for state in PetState
        }

        self.movie_size = {}
        self.load_gif_size()

        self.current_state = None
        self.pet_label = QLabel(self)
        self.init_window()

        self.tray_icon = QSystemTrayIcon()
        self.init_tary_icon()
        self.drag_position = QPoint()

        self.rand_move_interval = 10000
        self.rand_move_timer = QTimer(self)
        self.rand_move_timer.timeout.connect(self.start_random_move)
        self.rand_move_timer.start(self.rand_move_interval)
        self.move_timer = QTimer(self)
        self.move_timer.timeout.connect(self.perform_move)

        debug_timer = QTimer(self)
        debug_timer.timeout.connect(self.debug)
        debug_timer.start(1000)
        
    def load_gif_size(self):
        '''
        加载图像尺寸防止图像消失（真的有这个bug）
        '''
        for state in PetState:
            movie = self.movies[state]
            movie.jumpToFrame(0)
            size = movie.currentPixmap().size()
            self.movie_size[state] = size

    def init_window(self):
        '''
        初始化桌宠
        '''
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.SubWindow
        )

        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        self.switch_state(PetState.STANDBY)

        gif_size = self.movies[PetState.STANDBY].currentPixmap().size()
        self.resize(gif_size)
        self.pet_label.resize(gif_size)

        self.show()


    def init_tary_icon(self):
        '''
        初始化图标(windows隐藏的图标)
        '''
        icon_path = os.path.join(self.resource_path, 'standby.gif')
        self.tray_icon.setIcon(QIcon(icon_path))

        self.tray_icon.setToolTip("My LXB")

        tray_menu = QMenu(self)

        show_action = QAction("显示/隐藏", self)
        quit_action = QAction("退出", self)

        quit_action.triggered.connect(QApplication.instance().quit)
        show_action.triggered.connect(self.toggle_visibility)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
    
    def init_click_menu(self):
        '''
        正在施工中
        '''
        pass
        menu = QMenu(self)
        show_action = QAction("显示/隐藏", self)
        quit_action = QAction("退出", self)

        quit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(show_action)
        menu.addAction(quit_action)

    def toggle_visibility(self):
        if self.isVisible():
            self.hide()
            self.pet_label.hide()
        else :
            self.show()
            self.pet_label.show()

    def switch_state(self, state: PetState):
        if self.current_state == state:
            return
        # 停止先前的动画防止报错
        if self.current_state and self.current_state in self.movies:
            pre_movie = self.movies[self.current_state]
            pre_movie.stop()

        self.current_state = state
        cur_movie = self.movies[state]
        new_size = self.movie_size[state]

        if self.size() != new_size:
            self.resize(new_size)
            self.pet_label.resize(new_size)
            
        self.pet_label.setMovie(cur_movie)
        self.movies[state].start()

        print("shift to {cur_state.value}")

    def timer_reset(self, timer: QTimer):
        timer.stop()
        timer.start()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.switch_state(PetState.DRAG)
            self.drag_position = event.globalPosition().toPoint()-self.frameGeometry().topLeft()
            self.rand_move_timer.stop()
            event.accept()
        
        if event.button() == Qt.MouseButton.RightButton:
            menu = QMenu(self)
            
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.MouseButton.LeftButton and self.current_state == PetState.DRAG:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.switch_state(PetState.STANDBY)
            self.rand_move_timer.start()
            event.accept()

    def start_random_move(self):
        if self.current_state == PetState.STANDBY:
            self.switch_state(PetState.MOVE)
            self.rand_move_timer.stop()
            screen_geo = QApplication.primaryScreen().geometry()
            target_x = self.x() + random.randint(-150, 150)
            target_y = self.y() + random.randint(-150, 150)
            target_x = max(0, min(target_x, screen_geo.width() - self.width()))
            target_y = max(0, min(target_y, screen_geo.height() - self.height()))
            self.target_position = QPoint(target_x, target_y)
            self.move_timer.start(20)

    def perform_move(self):
        current_pos = self.pos()
        direction = self.target_position - current_pos
        if direction.manhattanLength() < 5:
            self.move(self.target_position)
            self.move_timer.stop()
            self.switch_state(PetState.STANDBY)
            self.rand_move_timer.start(self.rand_move_interval)
            return
        step = QVector2D(direction).normalized() * 5
        self.move(current_pos + QPoint(int(step.x()), int(step.y())))



    def debug(self):
        '''
        debug每秒钟输出一次的内容
        '''
        if self.isDebug:
            print(self.current_state.value)
            print(self.pet_label.movie)
            print(self.frameGeometry().topLeft())
        
    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pet = Deskpet()
    sys.exit(app.exec())

    


        
        

