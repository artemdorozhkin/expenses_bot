from datetime import date
from dataclasses import dataclass


@dataclass
class Expense:
    category: str
    amount: float
    created_at: date


@dataclass
class Category:
    name: str
