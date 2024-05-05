import re
from dataclasses import dataclass
from typing import List, Literal, Optional

Category = Literal["movies_at_home", "movies_in_theaters", "tv_series_browse"]
Sorting = Literal[
    "sort:a_z",
    "sort:popular",
    "sort:newest",
    "sort:critic_highest",
    "sort:critic_lowest",
    "sort:audience_highest",
    "sort:audience_lowest",
]
Genre = Literal[
    "action",
    "adventure",
    "animation",
    "anime",
    "biography",
    "comedy",
    "crime",
    "documentary",
    "drama",
    "entertainment",
    "faith_and_spirituality",
    "fantasy",
    "game_show",
    "health_and_wellness",
    "history",
    "holiday",
    "horror",
    "house_and_garden",
    "kids_and_family",
    "lgbtq",
    "music",
    "musical",
    "mystery_and_thriller",
    "nature",
    "news",
    "reality",
    "romance",
    "sci_fi",
    "short",
    "soap",
    "special_interest",
    "sports",
    "stand_up",
    "talk_show",
    "travel",
    "variety",
    "war",
    "western",
]
Rating = Literal["g", "nc_17", "nr", "pg", "pg_13", "r", "ur"]

MAX_PAGES = 10
BASE_URL = "https://www.rottentomatoes.com"
CATEGORIES: List[Category] = [
    "movies_at_home",
    "movies_in_theaters",
    "tv_series_browse",
]
SORTINGS: List[Sorting] = [
    "sort:a_z",
    "sort:popular",
    "sort:newest",
    "sort:critic_highest",
    "sort:critic_lowest",
    "sort:audience_highest",
    "sort:audience_lowest",
]
GENRES: List[Genre] = [
    "action",
    "adventure",
    "animation",
    "anime",
    "biography",
    "comedy",
    "crime",
    "documentary",
    "drama",
    "entertainment",
    "faith_and_spirituality",
    "fantasy",
    "game_show",
    "health_and_wellness",
    "history",
    "holiday",
    "horror",
    "house_and_garden",
    "kids_and_family",
    "lgbtq",
    "music",
    "musical",
    "mystery_and_thriller",
    "nature",
    "news",
    "reality",
    "romance",
    "sci_fi",
    "short",
    "soap",
    "special_interest",
    "sports",
    "stand_up",
    "talk_show",
    "travel",
    "variety",
    "war",
    "western",
]
RATINGS: List[Rating] = ["g", "nc_17", "nr", "pg", "pg_13", "r", "ur"]


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


def create_url(
    category: Category,
    sorting: Sorting,
    genre: Genre,
    rating: Rating,
) -> str:
    return f"{BASE_URL}/browse/{category}/genres:{genre}~ratings:{rating}~{sorting}"
