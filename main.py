import asyncio
import sys
import threading
import time

from PyQt6.QtWidgets import QApplication

from UIMain import Main
from core.engine import Engine

# def chart(snap):
#     print(snap)

engine = None

engine_set = asyncio.Event()

async def _main():
    global engine
    engine = Engine()

    engine_set.set()
    # engine.assign_chart_callback(chart)

    await engine.run()

def main():
    asyncio.run(_main())

if __name__ == '__main__':

    t = threading.Thread(target=main)
    t.start()

    app = QApplication(sys.argv)

    while True:
        if not engine_set.is_set():
            time.sleep(0.5)

        else:
            break

    print("Engine set!")
    w = Main(engine=engine)

    w.resize(1000, 600)

    w.show()
    sys.exit(app.exec())
