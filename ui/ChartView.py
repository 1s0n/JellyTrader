import collections
import queue
from typing import Iterable, List, Tuple, Optional

from PyQt6 import QtWidgets
from PyQt6.QtCore import QPointF, QRectF
from PyQt6.QtGui import QPicture, QPainter, QFont
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
import pyqtgraph as pg
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QGridLayout, QWidget, QLabel

from core.types import BookSnapshot, CandleSnapshot

OHLC = Tuple[float, float, float, float, float]  # (t, open, close, low, high)


class CandlestickItem(pg.GraphicsObject):
    def __init__(self, data: Iterable[OHLC] = ()):
        super().__init__()
        self.data: List[OHLC] = []
        self.picture = QPicture()
        self.setData(list(data))

    def setData(self, data: List[OHLC]) -> None:
        self.data = data
        self._generatePicture()
        self.prepareGeometryChange()
        self.update()

    def _generatePicture(self) -> None:
        self.picture = QPicture()
        p = QPainter(self.picture)

        w = 0.6  # candle width in x-units

        for (t, o, c, low, high) in self.data:
            up = c >= o
            pen = pg.mkPen("g" if up else "r", width=1)
            brush = pg.mkBrush("g" if up else "r")

            # wick
            p.setPen(pen)
            p.setBrush(pg.mkBrush(None))
            p.drawLine(QPointF(t, low), QPointF(t, high))

            # body
            top = c if up else o
            bot = o if up else c
            h = top - bot
            if h == 0:
                h = 1e-9

            p.setPen(pen)
            p.setBrush(brush)
            p.drawRect(QRectF(t - w / 2, bot, w, h))

        p.end()

    def paint(self, painter, *args) -> None:
        painter.drawPicture(0, 0, self.picture)

    def boundingRect(self) -> QRectF:
        return QRectF(self.picture.boundingRect())

class CandlestickChartWidget(QtWidgets.QWidget):
    """
    Drop-in QWidget candlestick chart.
    - Put it in any layout
    - Call set_ohlc(...) to replace data
    - Call append_candle(...) / update_last_candle(...) for live updates
    """
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None):
        super().__init__(parent)

        self.plot = pg.PlotWidget()
        self.plot.showGrid(x=True, y=True, alpha=0.25)
        self.plot.setMenuEnabled(True)
        self.plot.setMouseEnabled(x=True, y=True)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot)

        self._data: List[OHLC] = []
        self._candles = CandlestickItem(self._data)
        self.plot.addItem(self._candles)

    def set_ohlc(self, data: Iterable[OHLC], *, auto_range: bool = True) -> None:
        self._data = list(data)
        self._candles.setData(self._data)
        if auto_range:
            self.plot.enableAutoRange()

    def append_candle(self, candle: OHLC, *, auto_range: bool = True) -> None:
        self._data.append(candle)
        self._candles.setData(self._data)
        if auto_range:
            self.plot.enableAutoRange()

    def update_last_candle(self, candle: OHLC, *, auto_range: bool = False) -> None:
        if not self._data:
            self.append_candle(candle, auto_range=auto_range)
            return
        self._data[-1] = candle
        self._candles.setData(self._data)
        if auto_range:
            self.plot.enableAutoRange()

    def clear(self) -> None:
        self._data.clear()
        self._candles.setData(self._data)


class ChartViewPage(QWidget):
    def __init__(self, parent: Optional[QWidget] = None, l_callback = None, s_callback = None):
        super().__init__(parent)

        l = QVBoxLayout(self)

        title = QLabel("Chart view")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignLeft)

        longBTN = QPushButton("Long")
        longBTN.setStyleSheet("""
        QPushButton {
            background-color: #2e8b57;
            color: white;
            border-radius: 6px;
            font-size: 14px;
            padding: 10px 16px;
        }
        """)
        shortBTN = QPushButton("Short")



        self.chart = CandlestickChartWidget()
        l.addWidget(title)
        l.addWidget(self.chart)

        button_row = QHBoxLayout()
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_row.addWidget(longBTN)
        button_row.addSpacing(10)
        button_row.addWidget(shortBTN)



        l.addLayout(button_row)

        l.addStretch()
        self.setLayout(l)

        self.data_queue = queue.Queue()

    def update_graph(self, candle: CandleSnapshot):
        print("UPDATED")
        _candle = (candle.timestamp, candle.open, candle.close, candle.low, candle.high) # (t, open, close, low, high)

        self.data_queue.put(_candle)

class _MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widgets App")

        self.widget = ChartViewPage()

        self.setCentralWidget(self.widget)

# --- demo usage ---
if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    win = _MainWindow()

    # win.setCentralWidget(chart)

    demo = [
        (0, 100, 104, 98, 106),
        (1, 104, 101, 99, 105),
        (2, 101, 103, 100, 107),
        (3, 103, 110, 102, 112),
        (4, 110, 108, 107, 113),
    ]
    demo = []
    win.widget.chart.set_ohlc(demo)

    win.resize(900, 500)
    win.show()
    sys.exit(app.exec())
