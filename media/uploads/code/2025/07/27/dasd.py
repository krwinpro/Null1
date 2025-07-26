import sys
import json
import random
import keyboard
import os
import logging
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QListWidget, QLabel, QCheckBox, 
                             QLineEdit, QDialog, QDialogButtonBox, QMessageBox, QListWidgetItem,
                             QSpinBox, QSlider, QFileDialog, QComboBox, QStyledItemDelegate,
                             QStyle, QGraphicsDropShadowEffect)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QSize, QPropertyAnimation, QEasingCurve, QRectF, QRect
from PyQt6.QtGui import QColor, QPalette, QIcon, QFont, QPainter, QPainterPath, QLinearGradient
import time


logging.basicConfig(filename='macro_log.txt', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class StyleHelper:
    @staticmethod
    def get_dark_style():
        return """
        QMainWindow, QDialog {
            background: #1a1a1a;
            color: #e0e0e0;
        }
        
        QLabel, QCheckBox, QComboBox {
            color: #e0e0e0;
            font-size: 12px;
        }
        
        QPushButton {
            background: #2c2c2c;
            color: #e0e0e0;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
        }
        
        QPushButton:hover {
            background: #3a3a3a;
        }
        
        QPushButton:pressed {
            background: #1e1e1e;
        }
        
        QTextEdit, QListWidget, QLineEdit {
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #3a3a3a;
            border-radius: 3px;
            padding: 5px;
            font-size: 12px;
        }
        
        QTextEdit:focus, QListWidget:focus, QLineEdit:focus {
            border: 1px solid #4a4a4a;
        }
        
        QSpinBox {
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #3a3a3a;
            border-radius: 3px;
            padding: 2px 5px;
            font-size: 12px;
        }
        
        QSpinBox:focus {
            border: 1px solid #4a4a4a;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            width: 16px;
            background: #3a3a3a;
            border-radius: 2px;
        }
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background: #4a4a4a;
        }
        
        QComboBox {
            background-color: #2c2c2c;
            color: #e0e0e0;
            border: 1px solid #3a3a3a;
            border-radius: 3px;
            padding: 2px 5px;
            min-width: 6em;
        }
        
        QComboBox:focus {
            border: 1px solid #4a4a4a;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #e0e0e0;
        }
        
        QComboBox:hover {
            background-color: #3a3a3a;
        }
        
        QComboBox QAbstractItemView {
            background-color: #2c2c2c;
            color: #e0e0e0;
            selection-background-color: #4a4a4a;
            selection-color: #e0e0e0;
            border: 1px solid #4a4a4a;
        }
        
        QScrollBar:vertical {
            border: none;
            background: #2c2c2c;
            width: 8px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #4a4a4a;
            min-height: 20px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 2px;
            border: 1px solid #3a3a3a;
        }
        
        QCheckBox::indicator:checked {
            background-color: #4a4a4a;
            border: 1px solid #4a4a4a;
        }
        
        QCheckBox::indicator:unchecked:hover {
            border: 1px solid #4a4a4a;
        }
        """

    @staticmethod
    def get_light_style():
        return """
        QMainWindow, QDialog {
            background: #f0f0f0;
            color: #2c2c2c;
        }
        
        QLabel, QCheckBox, QComboBox {
            color: #2c2c2c;
            font-size: 12px;
        }
        
        QPushButton {
            background: #e0e0e0;
            color: #2c2c2c;
            border: none;
            padding: 5px 10px;
            border-radius: 3px;
            font-size: 12px;
        }
        
        QPushButton:hover {
            background: #d0d0d0;
        }
        
        QPushButton:pressed {
            background: #c0c0c0;
        }
        
        QTextEdit, QListWidget, QLineEdit {
            background-color: #ffffff;
            color: #2c2c2c;
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            padding: 5px;
            font-size: 12px;
        }
        
        QTextEdit:focus, QListWidget:focus, QLineEdit:focus {
            border: 1px solid #a0a0a0;
        }
        
        QSpinBox {
            background-color: #ffffff;
            color: #2c2c2c;
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            padding: 2px 5px;
            font-size: 12px;
        }
        
        QSpinBox:focus {
            border: 1px solid #a0a0a0;
        }
        
        QSpinBox::up-button, QSpinBox::down-button {
            width: 16px;
            background: #e0e0e0;
            border-radius: 2px;
        }
        
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background: #d0d0d0;
        }
        
        QComboBox {
            background-color: #ffffff;
            color: #2c2c2c;
            border: 1px solid #c0c0c0;
            border-radius: 3px;
            padding: 2px 5px;
            min-width: 6em;
        }
        
        QComboBox:focus {
            border: 1px solid #a0a0a0;
        }
        
        QComboBox::drop-down {
            border: none;
            width: 20px;
        }
        
        QComboBox::down-arrow {
            image: none;
            border-left: 4px solid transparent;
            border-right: 4px solid transparent;
            border-top: 4px solid #2c2c2c;
        }
        
        QComboBox:hover {
            background-color: #e0e0e0;
        }
        
        QComboBox QAbstractItemView {
            background-color: #ffffff;
            color: #2c2c2c;
            selection-background-color: #d0d0d0;
            selection-color: #2c2c2c;
            border: 1px solid #a0a0a0;
        }
        
        QScrollBar:vertical {
            border: none;
            background: #e0e0e0;
            width: 8px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background: #c0c0c0;
            min-height: 20px;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        QCheckBox::indicator {
            width: 16px;
            height: 16px;
            border-radius: 2px;
            border: 1px solid #c0c0c0;
        }
        
        QCheckBox::indicator:checked {
            background-color: #a0a0a0;
            border: 1px solid #a0a0a0;
        }
        
        QCheckBox::indicator:unchecked:hover {
            border: 1px solid #a0a0a0;
        }
        """

class ThemeComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedWidth(80)
        self.setFixedHeight(25)
        self.addItems(["Dark", "Light"])
        
        class ItemDelegate(QStyledItemDelegate):
            def paint(self, painter, option, index):
                painter.save()
                
                if option.state & QStyle.StateFlag.State_Selected:
                    painter.fillRect(option.rect, QColor("#3a3a3a" if index.data() == "Dark" else "#d0d0d0"))
                else:
                    painter.fillRect(option.rect, QColor("#2c2c2c" if index.data() == "Dark" else "#e0e0e0"))
                
                text_color = QColor("#e0e0e0" if index.data() == "Dark" else "#2c2c2c")
                painter.setPen(text_color)
                painter.setFont(option.font)
                painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, index.data())
                
                painter.restore()
                
        self.setItemDelegate(ItemDelegate())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        bg_color = QColor("#2c2c2c" if self.currentText() == "Dark" else "#e0e0e0")
        text_color = QColor("#e0e0e0" if self.currentText() == "Dark" else "#2c2c2c")
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(bg_color)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 3, 3)
        
        painter.setPen(text_color)
        painter.drawText(QRect(0, 0, self.width(), self.height()), Qt.AlignmentFlag.AlignCenter, self.currentText())

class ToggleButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setFixedSize(40, 20)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self.isChecked():
            brush = QColor("#4a4a4a")
        else:
            brush = QColor("#2c2c2c")

        pen = QColor("#3a3a3a")
        
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRoundedRect(0, 0, self.width(), self.height(), 10, 10)

        if self.isChecked():
            painter.setBrush(QColor("#e0e0e0"))
            painter.drawEllipse(self.width() - 18, 2, 16, 16)
        else:
            painter.setBrush(QColor("#e0e0e0"))
            painter.drawEllipse(2, 2, 16, 16)

class MacroThread(QThread):
    message_sent = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.active = False
        self.messages = []
        self.hotkey = "f2"
        self.auto_spacing = False
        self.auto_enter = False
        self.delay = 0.2
        self.random_delay = False
        self.min_delay = 0.1
        self.max_delay = 0.5
        self.big_mode = False
        self.mention_mode = False
        self.mention_id = ""
        self.recent_messages = []

    def run(self):
        prefix_added = False
        while True:
            if self.active and self.messages:
                if keyboard.is_pressed(self.hotkey):
                    available_messages = [msg for msg in self.messages if msg not in self.recent_messages]
                    if not available_messages:
                        available_messages = self.messages
                        self.recent_messages = []
            
                    message = random.choice(available_messages)
                    self.recent_messages.append(message)
                    if len(self.recent_messages) > 3:
                        self.recent_messages.pop(0)
            
                    formatted_message = ""
                    
                    if self.big_mode and self.mention_mode and self.mention_id:
                        formatted_message = f"# {self.mention_id} {message}"
                    elif self.big_mode:
                        formatted_message = f"# {message}"
                    elif self.mention_mode and self.mention_id:
                        formatted_message = f"{self.mention_id} {message}"
                    else:
                        formatted_message = message

                    if self.auto_spacing:
                        formatted_message += " "
                        
                    keyboard.write(formatted_message)
                    if self.auto_enter:
                        keyboard.press_and_release('enter')
                        prefix_added = False
                    self.message_sent.emit(formatted_message)
                    
                    if self.random_delay:
                        delay = random.uniform(self.min_delay, self.max_delay)
                    else:
                        delay = self.delay
                    self.msleep(int(delay * 1000))
                self.msleep(10)

class LoadingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Loading")
        self.setFixedSize(300, 100)
        layout = QVBoxLayout()
        self.label = QLabel("로딩시도중...")
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.steps = [
            "로딩시도중...",
            "화이트리스트 체크중...",
            "버전 체크...",
            "블랙리스트 체크..."
        ]
        self.current_step = 0
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_step)
        self.timer.start(2000)
    
    def update_step(self):
        if self.current_step < len(self.steps):
            self.label.setText(self.steps[self.current_step])
            self.current_step += 1
        else:
            self.label.setText("로딩 완료!")
            self.timer.stop()
            QTimer.singleShot(2000, self.accept)

    def show(self):
        super().show()
        loop = QEventLoop()
        self.accepted.connect(loop.quit)
        loop.exec()

class PremiumChatMacro(QMainWindow):
    def __init__(self):
        super().__init__()
        try:
            self.setWindowTitle("메크로")
            self.setGeometry(100, 100, 400, 600)
            self.current_theme = "dark"
            self.setStyleSheet(StyleHelper.get_dark_style())

            self.messages = []
            self.hotkey = "f2"
            self.auto_spacing = False
            self.auto_enter = False
            self.delay = 0.2
            self.random_delay = False
            self.min_delay = 0.1
            self.max_delay = 0.5
            self.big_mode = False
            self.mention_mode = False
            self.mention_id = ""

            self.macro_thread = MacroThread(self)
            self.macro_thread.message_sent.connect(self.update_recent_message)
            self.macro_thread.start()

            self.init_ui()
            self.load_settings()
        except Exception as e:
            logging.exception("Error in PremiumChatMacro initialization")
            QMessageBox.critical(self, "Initialization Error", f"An error occurred during initialization: {str(e)}")

    def init_ui(self):
        try:
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            main_layout = QVBoxLayout(central_widget)
            main_layout.setSpacing(10)
            main_layout.setContentsMargins(10, 10, 10, 10)

            
            self.message_list = QListWidget()
            self.message_list.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
            
            self.message_input = QTextEdit()
            self.message_input.setPlaceholderText("Enter your message here...")
            self.message_input.setMaximumHeight(100)

           
            theme_layout = QHBoxLayout()
            theme_label = QLabel("Theme:")
            self.theme_combo = ThemeComboBox()
            self.theme_combo.setCurrentText("Dark" if self.current_theme == "dark" else "Light")
            self.theme_combo.currentTextChanged.connect(self.change_theme)
            theme_layout.addWidget(theme_label)
            theme_layout.addWidget(self.theme_combo)
            theme_layout.addStretch()
            main_layout.addLayout(theme_layout)

          
            config_layout = QHBoxLayout()
            load_config_button = QPushButton("Load Config")
            load_config_button.clicked.connect(self.load_config)
            save_config_button = QPushButton("Save Config")
            save_config_button.clicked.connect(self.save_config)
            config_layout.addWidget(load_config_button)
            config_layout.addWidget(save_config_button)
            main_layout.addLayout(config_layout)

           
            control_group = QWidget()
            control_layout = QHBoxLayout(control_group)
            control_layout.setContentsMargins(0, 0, 0, 0)
            control_layout.setSpacing(5)
            control_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

            self.toggle_button = ToggleButton()
            self.toggle_button.clicked.connect(self.toggle_macro)
            control_layout.addWidget(self.toggle_button)

            self.status_label = QLabel("●")
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 14px;")
            self.status_label.setContentsMargins(0, 0, 0, 2)
            control_layout.addWidget(self.status_label)

            control_layout.addStretch()
            main_layout.addWidget(control_group)
            hotkey_layout = QHBoxLayout()
            self.hotkey_label = QLabel("Hotkey:")
            self.hotkey_input = QLineEdit(self.hotkey)
            self.hotkey_input.textChanged.connect(self.update_hotkey)
            hotkey_layout.addWidget(self.hotkey_label)
            hotkey_layout.addWidget(self.hotkey_input)
            main_layout.addLayout(hotkey_layout)

            
            delay_layout = QHBoxLayout()
            delay_label = QLabel("Delay (ms):")
            self.delay_spin = QSpinBox()
            self.delay_spin.setRange(1, 1000)
            self.delay_spin.setValue(int(self.delay * 1000))
            self.delay_spin.valueChanged.connect(self.update_delay)
            
            minus_button = QPushButton("-")
            minus_button.setFixedSize(20, 20)
            minus_button.clicked.connect(lambda: self.delay_spin.setValue(self.delay_spin.value() - 1))

            plus_button = QPushButton("+")
            plus_button.setFixedSize(20, 20)
            plus_button.clicked.connect(lambda: self.delay_spin.setValue(self.delay_spin.value() + 1))

            delay_layout.addWidget(delay_label)
            delay_layout.addWidget(minus_button)
            delay_layout.addWidget(self.delay_spin)
            delay_layout.addWidget(plus_button)
            main_layout.addLayout(delay_layout)

            
            random_delay_layout = QHBoxLayout()
            self.random_delay_checkbox = QCheckBox("Random Delay")
            self.random_delay_checkbox.stateChanged.connect(self.toggle_random_delay)
            random_delay_layout.addWidget(self.random_delay_checkbox)
            main_layout.addLayout(random_delay_layout)

            
            min_max_delay_layout = QHBoxLayout()
            min_delay_label = QLabel("Min Delay:")
            self.min_delay_spin = QSpinBox()
            self.min_delay_spin.setRange(1, 1000)
            self.min_delay_spin.setValue(int(self.min_delay * 1000))
            self.min_delay_spin.valueChanged.connect(self.update_min_delay)
            max_delay_label = QLabel("Max Delay:")
            self.max_delay_spin = QSpinBox()
            self.max_delay_spin.setRange(1, 1000)
            self.max_delay_spin.setValue(int(self.max_delay * 1000))
            self.max_delay_spin.valueChanged.connect(self.update_max_delay)
            min_max_delay_layout.addWidget(min_delay_label)
            min_max_delay_layout.addWidget(self.min_delay_spin)
            min_max_delay_layout.addWidget(max_delay_label)
            min_max_delay_layout.addWidget(self.max_delay_spin)
            main_layout.addLayout(min_max_delay_layout)

        
            auto_options = QWidget()
            auto_layout = QVBoxLayout(auto_options)
            auto_layout.setSpacing(4)
            auto_layout.setContentsMargins(0, 0, 0, 0)
            
            self.auto_spacing_checkbox = QCheckBox("Auto Space")
            self.auto_spacing_checkbox.stateChanged.connect(self.toggle_auto_spacing)
            
            self.auto_enter_checkbox = QCheckBox("Auto Enter")
            self.auto_enter_checkbox.stateChanged.connect(self.toggle_auto_enter)
            
            auto_layout.addWidget(self.auto_spacing_checkbox)
            auto_layout.addWidget(self.auto_enter_checkbox)
            main_layout.addWidget(auto_options)

        
            big_mode_container = QWidget()
            big_mode_layout = QHBoxLayout(big_mode_container)
            big_mode_layout.setContentsMargins(0, 0, 0, 0)
            big_mode_layout.setSpacing(10)
            
            big_mode_label = QLabel("BIG MODE:")
            self.big_mode_toggle = ToggleButton()
            self.big_mode_toggle.clicked.connect(self.toggle_big_mode)
            
            big_mode_layout.addWidget(big_mode_label)
            big_mode_layout.addWidget(self.big_mode_toggle)
            big_mode_layout.addStretch()
            main_layout.addWidget(big_mode_container)

            
            mention_mode_container = QWidget()
            mention_mode_layout = QHBoxLayout(mention_mode_container)
            mention_mode_layout.setContentsMargins(0, 0, 0, 0)
            mention_mode_layout.setSpacing(10)
            
            mention_mode_label = QLabel("Mention Mode:")
            self.mention_mode_toggle = ToggleButton()
            self.mention_mode_toggle.clicked.connect(self.toggle_mention_mode)
            
            mention_mode_layout.addWidget(mention_mode_label)
            mention_mode_layout.addWidget(self.mention_mode_toggle)
            mention_mode_layout.addStretch()
            main_layout.addWidget(mention_mode_container)

           
            mention_id_layout = QHBoxLayout()
            mention_id_label = QLabel("Mention ID:")
            self.mention_id_input = QLineEdit(self.mention_id)
            self.mention_id_input.textChanged.connect(self.update_mention_id)
            mention_id_layout.addWidget(mention_id_label)
            mention_id_layout.addWidget(self.mention_id_input)
            main_layout.addLayout(mention_id_layout)

          
            main_layout.addWidget(self.message_input)
            add_button = QPushButton("Add Message")
            add_button.clicked.connect(self.add_message)
            main_layout.addWidget(add_button)

     
            main_layout.addWidget(self.message_list)

            
            list_controls = QHBoxLayout()
            remove_button = QPushButton("Remove Selected")
            remove_button.clicked.connect(self.remove_selected_messages)
            list_controls.addWidget(remove_button)

            clear_button = QPushButton("Clear All")
            clear_button.clicked.connect(self.clear_all_messages)
            list_controls.addWidget(clear_button)
            main_layout.addLayout(list_controls)

          
            self.recent_message_label = QLabel("Recent: None")
            main_layout.addWidget(self.recent_message_label)

            
            self.apply_shadow_effect()

        except Exception as e:
            logging.exception("Error in init_ui")
            QMessageBox.critical(self, "UI Initialization Error", f"An error occurred while initializing the UI: {str(e)}")

    def apply_shadow_effect(self):
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))

        for widget in self.findChildren(QWidget):
            if isinstance(widget, (QPushButton, QLineEdit, QTextEdit, QListWidget, QComboBox)):
                widget.setGraphicsEffect(shadow)

    def change_theme(self, theme):
        self.current_theme = "dark" if theme == "Dark" else "light"
        self.setStyleSheet(
            StyleHelper.get_dark_style() if self.current_theme == "dark" 
            else StyleHelper.get_light_style()
        )

    def load_config(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Load Config", "", "JSON Files (*.json)")
        if file_name:
            try:
                with open(file_name, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                self.apply_config(config)
                QMessageBox.information(self, "Config Loaded", f"Loaded config from {file_name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to load config: {str(e)}")

    def save_config(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Config", "", "JSON Files (*.json)")
        if file_name:
            config = self.get_current_config()
            try:
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(config, f, ensure_ascii=False, indent=2)
                QMessageBox.information(self, "Config Saved", f"Saved config to {file_name}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save config: {str(e)}")

    def apply_config(self, config):
        self.messages = config.get('messages', [])
        self.message_list.clear()
        self.message_list.addItems(self.messages)
        self.hotkey = config.get('hotkey', 'f2')
        self.hotkey_input.setText(self.hotkey)
        self.auto_spacing = config.get('auto_spacing', False)
        self.auto_spacing_checkbox.setChecked(self.auto_spacing)
        self.auto_enter = config.get('auto_enter', False)
        self.auto_enter_checkbox.setChecked(self.auto_enter)
        self.delay = config.get('delay', 0.2)
        self.delay_spin.setValue(int(self.delay * 1000))
        self.random_delay = config.get('random_delay', False)
        self.random_delay_checkbox.setChecked(self.random_delay)
        self.min_delay = config.get('min_delay', 0.1)
        self.min_delay_spin.setValue(int(self.min_delay * 1000))
        self.max_delay = config.get('max_delay', 0.5)
        self.max_delay_spin.setValue(int(self.max_delay * 1000))
        self.big_mode = config.get('big_mode', False)
        self.big_mode_toggle.setChecked(self.big_mode)
        self.mention_mode = config.get('mention_mode', False)
        self.mention_mode_toggle.setChecked(self.mention_mode)
        self.mention_id = config.get('mention_id', '')
        self.mention_id_input.setText(self.mention_id)
        self.current_theme = config.get('theme', 'dark')
        self.theme_combo.setCurrentText("Dark" if self.current_theme == "dark" else "Light")

        self.update_macro_thread()

    def get_current_config(self):
        return {
            "messages": [self.message_list.item(i).text() for i in range(self.message_list.count())],
            "hotkey": self.hotkey,
            "auto_spacing": self.auto_spacing,
            "auto_enter": self.auto_enter,
            "delay": self.delay,
            "random_delay": self.random_delay,
            "min_delay": self.min_delay,
            "max_delay": self.max_delay,
            "big_mode": self.big_mode,
            "mention_mode": self.mention_mode,
            "mention_id": self.mention_id,
            "theme": self.current_theme
        }

    def update_macro_thread(self):
        self.macro_thread.messages = self.messages
        self.macro_thread.hotkey = self.hotkey
        self.macro_thread.auto_spacing = self.auto_spacing
        self.macro_thread.auto_enter = self.auto_enter
        self.macro_thread.delay = self.delay
        self.macro_thread.random_delay = self.random_delay
        self.macro_thread.min_delay = self.min_delay
        self.macro_thread.max_delay = self.max_delay
        self.macro_thread.big_mode = self.big_mode
        self.macro_thread.mention_mode = self.mention_mode
        self.macro_thread.mention_id = self.mention_id

    def toggle_macro(self):
        try:
            self.macro_thread.active = self.toggle_button.isChecked()
            if self.macro_thread.active:
                self.status_label.setStyleSheet("color: #2ecc71; font-weight: bold; font-size: 14px;")
            else:
                self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 14px;")
        except Exception as e:
            logging.exception("Error in toggle_macro")
            self.macro_thread.active = False
            self.toggle_button.setChecked(False)
            self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold; font-size: 14px;")
            QMessageBox.warning(self, "Error", f"Failed to toggle macro: {str(e)}")

    def update_hotkey(self):
        self.hotkey = self.hotkey_input.text().lower()
        self.macro_thread.hotkey = self.hotkey
        self.save_settings()

    def update_delay(self):
        self.delay = self.delay_spin.value() / 1000
        self.macro_thread.delay = self.delay
        self.save_settings()

    def toggle_random_delay(self, state):
        self.random_delay = state == Qt.CheckState.Checked.value
        self.macro_thread.random_delay = self.random_delay
        self.min_delay_spin.setEnabled(self.random_delay)
        self.max_delay_spin.setEnabled(self.random_delay)
        self.save_settings()

    def update_min_delay(self):
        self.min_delay = self.min_delay_spin.value() / 1000
        self.macro_thread.min_delay = self.min_delay
        self.save_settings()

    def update_max_delay(self):
        self.max_delay = self.max_delay_spin.value() / 1000
        self.macro_thread.max_delay = self.max_delay
        self.save_settings()

    def toggle_auto_spacing(self, state):
        self.auto_spacing = state == Qt.CheckState.Checked.value
        self.macro_thread.auto_spacing = self.auto_spacing
        self.save_settings()

    def toggle_auto_enter(self, state):
        self.auto_enter = state == Qt.CheckState.Checked.value
        self.macro_thread.auto_enter = self.auto_enter
        self.save_settings()

    def toggle_big_mode(self):
        self.big_mode = self.big_mode_toggle.isChecked()
        self.macro_thread.big_mode = self.big_mode
        self.save_settings()

    def toggle_mention_mode(self):
        self.mention_mode = self.mention_mode_toggle.isChecked()
        self.macro_thread.mention_mode = self.mention_mode
        self.save_settings()

    def update_mention_id(self):
        self.mention_id = self.mention_id_input.text()
        self.macro_thread.mention_id = self.mention_id
        self.save_settings()

    def add_message(self):
        message = self.message_input.toPlainText().strip()
        if message:
            self.messages.append(message)
            self.message_list.addItem(message)
            self.message_input.clear()
            self.macro_thread.messages = self.messages
            self.save_settings()

    def remove_selected_messages(self):
        selected_items = self.message_list.selectedItems()
        if not selected_items:
            return
        
        for item in selected_items:
            self.messages.remove(item.text())
            self.message_list.takeItem(self.message_list.row(item))
        
        self.macro_thread.messages = self.messages
        self.save_settings()

    def clear_all_messages(self):
        confirm = QMessageBox.question(
            self, 
            "Clear All Messages",
            "Are you sure you want to clear all messages?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            self.messages.clear()
            self.message_list.clear()
            self.macro_thread.messages = self.messages
            self.save_settings()

    def update_recent_message(self, message):
        self.recent_message_label.setText(f"Recent: {message}")

    def save_settings(self):
        settings = self.get_current_config()
        try:
            with open("macro_settings.json", "w", encoding="utf-8") as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logging.exception("Failed to save settings")
            QMessageBox.warning(self, "Error", f"Failed to save settings: {str(e)}")

    def load_settings(self):
        try:
            with open("macro_settings.json", "r", encoding="utf-8") as f:
                settings = json.load(f)
            self.apply_config(settings)
        except FileNotFoundError:
            logging.warning("Settings file not found. Using default settings.")
        except json.JSONDecodeError:
            logging.exception("Failed to load settings: Invalid JSON file")
            QMessageBox.warning(self, "Error", "Failed to load settings: Invalid JSON file")
        except Exception as e:
            logging.exception("Failed to load settings")
            QMessageBox.warning(self, "Error", f"Failed to load settings: {str(e)}")

    def closeEvent(self, event):
        try:
            self.macro_thread.active = False
            self.macro_thread.quit()
            self.macro_thread.wait()
            event.accept()
        except Exception as e:
            logging.exception("Error during application close")
            QMessageBox.critical(self, "Close Error", f"An error occurred while closing the application: {str(e)}")
            event.ignore()

def main():
    try:
        app = QApplication(sys.argv)
        
        print("로딩시도중...")
        time.sleep(0.01)
        print("화이트리스트 체크중...")
        time.sleep(0.001)
        print("버전 체크...")
        time.sleep(0.001)
        print("블랙리스트 체크...")
        time.sleep(0.001)
        print("로딩 완료!")
        
        window = PremiumChatMacro()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        logging.exception("Unhandled exception in main")
        print(f"Critical Error: An unhandled error occurred: {str(e)}")

if __name__ == "__main__":
    main()

