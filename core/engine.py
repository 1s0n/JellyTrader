import queue
import time

from core.types import CandleSnapshot
from data.crypto import CryptoStream
from core.utils import calculate_candle
from collections import deque
import asyncio
import sys

class Engine:
    def __init__(self):

        self.stream_queue = asyncio.Queue()
        self.data_deque = deque() # Max 10 updates per second, and we want to store last hour of data, approx. 864 kb of memory usage i think
        self.max_queue_size = 18000

        self.candle_queue = queue.Queue()

        self._stop = asyncio.Event()
        self.stream = CryptoStream(symbol="BTCUSDT", depth=20, debug=True)

        self.producer = asyncio.create_task(self.stream.run(self.stream_queue))

        # Callbacks
        self.chart_callback = None

    def stop(self):
        self._stop.set()

    def assign_chart_callback(self, callback):
        self.chart_callback = callback # TODO: Create object thats less fat to pass on instead of the whole snapshot

    async def run(self):

        interval1 = 1
        interval2 = 15

        timer1 = time.perf_counter() + interval1 # One second interval
        timer2 = time.perf_counter() + interval2 # 15 second interval
        try:
            while not self._stop.is_set():
                snap = await self.stream_queue.get()


                # 1H History deque
                if len(self.data_deque) >= self.max_queue_size:
                    self.data_deque.popleft()

                self.data_deque.append(snap)


                now = time.perf_counter()
                if now >= timer1:
                    # 1 second interval
                    # print("ONE SECOND")
                    candle = calculate_candle(self.data_deque, timeframe=1)
                    # print(candle)
                    self.chart_callback(candle)
                    # print("FINISHED ONE SECOND")
                    timer1 += interval1

                elif now >= timer2:
                    # print("15s")
                    timer2 += interval2

        except KeyboardInterrupt:
            self.stream.stop()
            await self.producer

async def _main():
    engine = Engine()
    await engine.run()

if __name__ == "__main__":
    asyncio.run(_main())