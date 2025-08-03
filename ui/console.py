from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QPushButton
from PyQt6.QtGui import QColor, QTextCursor, QTextBlockFormat
from PyQt6.QtCore import Qt
import logging
import enum


class LogLevel(enum.Enum):
    FATAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARN = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG


class ConsoleUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.all_logs = []
        self.active_filters = set(LogLevel)
        self.level_counts = {level: 0 for level in LogLevel}
        self.level_colors = {
            LogLevel.DEBUG: QColor("#808080"),
            LogLevel.INFO: QColor("#000000"),
            LogLevel.WARN: QColor("#d39c3f"),
            LogLevel.ERROR: QColor("#d84a4a"),
            LogLevel.FATAL: QColor("#800080"), 
        }
        
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle("日志控制台")
        self.setGeometry(100, 100, 800, 600)
        
        main_layout = QVBoxLayout(self)
        
        top_bar_layout = QHBoxLayout()
        self.filter_buttons = {}
        
        for level in LogLevel:

            button = QPushButton(f"{level.name}: 0")
            button.setCheckable(True) 
            button.setChecked(True) 
            
            button.setStyleSheet(f"""
                QPushButton {{
                    background-color: {self.level_colors[level].name()};
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 4px;
                }}
                QPushButton:checked {{
                    border: 2px solid #55aaff;
                }}
                QPushButton:hover {{
                    background-color: {self.level_colors[level].darker(120).name()};
                }}
            """)
            
            button.clicked.connect(lambda checked, lvl=level: self.on_filter_button_clicked(lvl))
            
            self.filter_buttons[level] = button
            top_bar_layout.addWidget(button)
            
        top_bar_layout.addStretch()
        main_layout.addLayout(top_bar_layout)
        
        self.log_display = QTextEdit()
        self.log_display.setReadOnly(True)
        main_layout.addWidget(self.log_display)

        bottom_bar_layout = QHBoxLayout()
        clear_button = QPushButton("清除")
        clear_button.clicked.connect(self.clear_logs)
        bottom_bar_layout.addStretch()
        bottom_bar_layout.addWidget(clear_button)
        main_layout.addLayout(bottom_bar_layout)

    def append_log(self, level: LogLevel, message: str):
        """接收日志信号，存储并根据当前筛选决定是否显示"""
        message_to_send = f"[{level.name}] : {message}"
        
        self.all_logs.append((level, message_to_send))
        
        self.level_counts[level] += 1
        self.filter_buttons[level].setText(f"{level.name}: {self.level_counts[level]}")        

        if level in self.active_filters:
            self._display_log_message(level, message_to_send)
        
        print(message_to_send)

    def _display_log_message(self, level: LogLevel, message: str):
        """
        一个专门负责向QTextEdit添加带颜色文本的函数
        """
        self.log_display.moveCursor(QTextCursor.MoveOperation.End)
        char_format = self.log_display.currentCharFormat()
        char_format.setForeground(self.level_colors.get(level, QColor("black")))
        self.log_display.setCurrentCharFormat(char_format)
        
        self.log_display.insertPlainText(message + '\n')
        self.log_display.ensureCursorVisible()

    def on_filter_button_clicked(self, level: LogLevel):
        """当筛选按钮被点击时触发"""
        button = self.filter_buttons[level]
        if button.isChecked():
            self.active_filters.add(level)
        else:
            self.active_filters.discard(level)
            
        self.refresh_display()

    def refresh_display(self):
        """根据当前的 active_filters 重新渲染整个日志显示区域"""
        self.log_display.clear()
        
        for level, message in self.all_logs:
            if level in self.active_filters:
                self._display_log_message(level, message)

    def clear_logs(self):
        """清除所有日志记录和显示"""
        self.all_logs.clear()
        self.level_counts = {level: 0 for level in LogLevel}
        
        self.log_display.clear()
        for level, button in self.filter_buttons.items():
            button.setText(f"{level.name}: {self.level_counts[level]}")


class Logger:
    def __init__(self):
        self.Console = ConsoleUI()

    def fatal(self, msg):
        self.Console.append_log(LogLevel.FATAL, msg)
    
    def error(self, msg):
        self.Console.append_log(LogLevel.ERROR, msg)

    def warn(self, msg):
        self.Console.append_log(LogLevel.WARN, msg)
    
    def info(self, msg):
        self.Console.append_log(LogLevel.INFO, msg)
    
    def debug(self, msg):
        self.Console.append_log(LogLevel.DEBUG, msg)

    def show(self):
        self.Console.show()
    
    def hide(self):
        self.Console.hide()


logger = Logger()



