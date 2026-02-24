from PyQt6.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QLabel
import sys
from ui.ChartView import ChartViewPage
from ui.StartPage import StartPage
import threading
from core.engine import Engine

class Main(QMainWindow):
    def __init__(self, engine: Engine):
        super().__init__()
        tabs = QTabWidget()

        p1 = StartPage()

        self.chart = ChartViewPage()
        engine.assign_chart_callback(self.chart.update_graph)

        tabs.addTab(p1, "Start")
        tabs.addTab(self.chart, "Chart")
        self.setCentralWidget(tabs)


#
# if __name__ == "__main__":
#
#     app = QApplication(sys.argv)
#     # w = Main()
#
#     w.resize(1000, 600)
#
#     w.show()
#     sys.exit(app.exec())
