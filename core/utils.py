import collections
import time
from core.types import BookSnapshot, Level, CandleSnapshot

def calculate_candle(data_deque: collections.deque, timeframe=1) -> CandleSnapshot:
    # l = 0
    # r = len(data_deque) - 1
    #
    # cutoff = time.time() - timeframe
    #
    # while l <= r:
    #     mid = (l + r) // 2
    #
    #     if data_deque[mid].timestamp < cutoff:
    #         l = mid + 1
    #     else:
    #         r = mid - 1
    #
    # start_index = l

    # print("Calculating candle...")
    cutoff = time.time() - timeframe
    recent = []

    for s in reversed(data_deque):
        if s.timestamp < cutoff:
            break
        recent.append(s)

    recent.reverse()
    # print("Finished reverse scan")
    # print(start_index)

    open_price = get_mid_price(recent[0])
    close_price = get_mid_price(recent[-1])
    highest_price = 0
    lowest_price = open_price

    for i in recent:

        p = get_mid_price(i)

        if p > highest_price:
            highest_price = p

        if p < lowest_price:
            lowest_price = p

    candle = CandleSnapshot(timestamp=time.time(), open=open_price, close=close_price, high=highest_price, low=lowest_price)
    return candle

def get_mid_price(snap: BookSnapshot):
    _bid = snap.bids[0].price
    _ask = snap.asks[0].price

    return (_bid + _ask) / 2