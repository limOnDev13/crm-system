from dataclasses import dataclass
from typing import Dict


@dataclass
class AdsStatistics:
    name: str
    leads_count: int
    customers_count: int
    profit: float


@dataclass
class TotalStatistics:
    products_count: int
    advertisements_count: int
    leads_count: int
    customers_count: int

    def to_dict(self) -> Dict[str, int]:
        return {
            "products_count": self.products_count,
            "advertisements_count": self.advertisements_count,
            "leads_count": self.leads_count,
            "customers_count": self.customers_count,
        }
