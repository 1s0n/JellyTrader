from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

mode_colours = {"live": "red", "paper": "orange", "backtest": "green"}

class StartPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        # layout.setSpacing(1)

        title = QLabel("JellyTrader v2")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        mode = "paper"
        modelab = QLabel()
        modelab.setText(f'Mode: <span style="color:{mode_colours[mode.lower()]};">{mode}</span>')
        modelab.setAlignment(Qt.AlignmentFlag.AlignLeft)
        modelab.setStyleSheet("color: white; font-size: 14px;")

        stralab = QLabel("Strategy: ")
        stralab.setAlignment(Qt.AlignmentFlag.AlignLeft)
        stralab.setStyleSheet("color: white; font-size: 14px;")

        marketlab = QLabel("Market: ")
        marketlab.setAlignment(Qt.AlignmentFlag.AlignLeft)
        marketlab.setStyleSheet("color: white; font-size: 14px;")

        # Add to layout
        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(modelab)
        layout.addWidget(stralab)
        layout.addWidget(marketlab)
        layout.addStretch()