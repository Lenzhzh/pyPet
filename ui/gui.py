import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QLineEdit, 
                             QComboBox, QCheckBox, QPushButton, QHBoxLayout,
                             QScrollArea)
from PyQt6.QtCore import Qt


class SettingUI(QWidget):
    '''
    设置界面，支持扩展，通过 ./setting.json 进行扩展。
    '''
    def __init__(self, manager, parents=None):
        super().__init__()
        self.manager = manager
        self.widgets = {}

        self.init_ui()
        self.load_settings()
        
    def init_ui(self):
        self.setWindowTitle("设置面板")

        top_layout = QVBoxLayout(self)
        self.setLayout(top_layout)

        scroller = QScrollArea()
        scroller.setWidgetResizable(True)
        top_layout.addWidget(scroller)

        content = QWidget()
        content_layout = QVBoxLayout(content)
        scroller.setWidget(content)
        content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 加载设置项
        schema = self.manager.get_schema()
        for item in schema:
             self.generate_setting_item(item, content_layout)

        # 保存和取消按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        save_button = QPushButton('保存并退出', self)
        cancel_button = QPushButton('关闭', self)

        save_button.clicked.connect(self.save_settings)
        cancel_button.clicked.connect(self.close)

        top_layout.addLayout(button_layout)

        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)


    def generate_setting_item(self, item, layout: QVBoxLayout):
        '''
        加载单个设置项
        '''
        item_id = item['id']
        label = item['label']
        item_type = item['type']
        lbl = QLabel(label)
        if item_type == 'checkBox':
            widget = QCheckBox(self)
        
        elif item_type == 'lineEdit':
            widget = QLineEdit(self)
            
        elif item_type == 'comboBox':
            widget = QComboBox(self)
            for display_name, internal_value in item['options'].items():
                widget.addItem(display_name, internal_value)
        else :
            print(f"Warn: {item_id} item widget didn't generate correctly, please check your item_type '{item_type}' !")
            return

        layout.addWidget(lbl)
        layout.addWidget(widget)
        self.widgets[item_id] = widget

        layout.addSpacing(10)
            
    def load_settings(self):
        '''
        加载现有设置
        '''
        for item_id, widget in self.widgets.items():
            value = self.manager.get(item_id)
            if isinstance(widget, QCheckBox):
                widget.setChecked(bool(value))
            
            elif isinstance(widget, QLineEdit):
                widget.setText(str(value))
            
            elif isinstance(widget, QComboBox):
                index = widget.findData(value)
                if index != -1:
                    widget.setCurrentIndex(index)
                else :
                    widget.setCurrentIndex(0)
                    print("INFO: Setting {item_id} have no current value, default setting are loaded !")
                
            else :
                print("Warn: Setting {item_id} haven't been loaded, please check it's item type !")

    def save_settings(self):
        '''
        将预设保存
        '''
        for item_id, widget in self.widgets.items():
            if isinstance(widget, QCheckBox):
                self.manager.set(item_id, widget.isChecked())
            elif isinstance(widget, QLineEdit):
                self.manager.set(item_id, widget.text())
            else :
                self.manager.set(item_id, widget.currentData())
        
        self.manager.save()
        sys.exit()