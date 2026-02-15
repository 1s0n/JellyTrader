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