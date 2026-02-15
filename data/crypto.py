import asyncio
import json
import time
from core.types import Level, BookSnapshot

import websockets


ws_url = "wss://stream.binance.com:9443/stream?streams={streamname}@depth"




class CryptoStream:
    def __init__(self, symbol: str, depth: int = 20, debug: bool = False):
        self.symbol = symbol
        self.depth = depth

        self._stop = asyncio.Event()
        self._ws = None

        self.reconnect_delay = 1
        self._debug = debug

    def stop(self):
        self._stop.set()

    async def run(self, out_queue: asyncio.Queue[BookSnapshot]):
        url = f"wss://stream.binance.com:9443/ws/{self.symbol.lower()}@depth{self.depth}@100ms"

        delay = self.reconnect_delay

        while not self._stop.is_set():
            try:
                async with websockets.connect(url, ping_interval=20, ping_timeout=20) as ws:

                    if self._debug:
                        print("Connected to Binance Websocket")

                    delay = self.reconnect_delay

                    self._ws = ws

                    async for msg in ws:
                        if self._stop.is_set():
                            break

                        data = json.loads(msg)
                        # print(data)
                        _bids = data.get("bids", [])
                        _asks = data.get("asks", [])

                        bids = []
                        asks = []

                        for price, vol in _bids:
                            if float(vol) > 0:
                                bids.append(Level(float(price), float(vol)))

                        for price, vol in _asks:
                            if float(vol) > 0:
                                asks.append(Level(float(price), float(vol)))

                        bids.sort(key=lambda x: x.price, reverse=True)
                        asks.sort(key=lambda x: x.price)

                        snapshot = BookSnapshot(timestamp=time.time(), bids=bids, asks=asks)
                        try:
                            out_queue.put_nowait(snapshot)
                        except asyncio.QueueFull:
                            try:
                                _ = out_queue.get_nowait()
                            except asyncio.QueueEmpty:
                                # print("Queue empty")
                                pass
                            try:
                                out_queue.put_nowait(snapshot)
                            except asyncio.QueueFull:
                                # print("Queue empty")
                                pass
            except Exception as e:
                print(e)
                await asyncio.sleep(delay)
                delay *= 2

        self._ws = None

async def _main():
    q: asyncio.Queue[BookSnapshot] = asyncio.Queue(maxsize=10)
    stream = CryptoStream(symbol="BTCUSDT", depth=20, debug=True)

    producer = asyncio.create_task(stream.run(q))

    print("Starting...")

    try:
        while True:
            snap = await q.get()
            if not snap.bids or not snap.asks:
                # print(snap)
                continue
            bb, ba = snap.bids[0].price, snap.asks[0].price
            print(f"{snap.timestamp:.3f}  bid={bb:.2f}  ask={ba:.2f}  spread={ba - bb:.2f}")
    except KeyboardInterrupt:
        stream.stop()
        await producer

if __name__ == "__main__":
    asyncio.run(_main())