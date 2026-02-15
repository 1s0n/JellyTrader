from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
import sys
from ui.ChartView import ChartViewPage
from ui.StartPage import StartPage

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        tabs = QTabWidget()

        p1 = StartPage()

        p2 = ChartViewPage()

        tabs.addTab(p1, "Start")
        tabs.addTab(p2, "Chart")
        self.setCentralWidget(tabs)

app = QApplication(sys.argv)
w = Main(); w.resize(1000, 600); w.show()
sys.exit(app.exec())
