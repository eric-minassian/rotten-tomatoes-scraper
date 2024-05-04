import re
from dataclasses import dataclass
from typing import List, Optional


def parse_currency_to_number(text: str) -> Optional[int]:
    # Regular expression to match a currency value with an optional M/B suffix
    pattern = r"[\$\€\£\¥]\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)([MB]?)"
    match = re.search(pattern, text)
    if match:
        amount, multiplier = match.groups()
        number = float(amount.replace(",", ""))
        # Adjust number based on the multiplier
        if multiplier == "M":
            number *= 1_000_000
        elif multiplier == "B":
            number *= 1_000_000_000
        return int(number)
    return None


@dataclass
class Score:
    average_rating: float
    banded_rating_count: str
    liked_count: int
    not_liked_count: int
    review_count: int
    score: int
    sentiment: str


@dataclass
class Media:
    title: str
    description: str
    audience_score: Optional[Score]
    critic_score: Optional[Score]
    director: Optional[List[str]]
    producer: Optional[List[str]]
    screenwriter: Optional[List[str]]
    distributor: Optional[List[str]]
    production_company: Optional[List[str]]
    genre: Optional[List[str]]
    sound_mix: Optional[List[str]]
    rating: Optional[str]
    original_language: Optional[str]
    release_date_theater: Optional[str]
    release_date_streaming: Optional[str]
    runtime: Optional[str]
    box_office: Optional[int]
