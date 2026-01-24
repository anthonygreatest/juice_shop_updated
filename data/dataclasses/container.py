from dataclasses import dataclass
from typing import Optional


@dataclass
class Password:
    password: str


@dataclass
class CreditCard:

    full_name: str
    card_num: int
    exp_month: str
    exp_year: str

@dataclass
class ProfileName:

    username: str
