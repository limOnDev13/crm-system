from dataclasses import dataclass


@dataclass
class AdsStatistics:
    name: str
    leads_count: int
    customers_count: int
    profit: float
