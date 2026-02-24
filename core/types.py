from dataclasses import dataclass
from typing import List


@dataclass
class Level:
    price: float
    volume: float

@dataclass
class BookSnapshot:
    timestamp: float
    bids: List[Level]
    asks: List[Level]

# @dataclass
# class LiteSnapshot:
#     timestamp: float
#     best_bid: float
#     best_ask: float

@dataclass
class CandleSnapshot:
    timestamp: float
    open: float
    close: float
    high: float
    low: float
    