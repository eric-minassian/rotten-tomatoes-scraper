import csv
import re
from dataclasses import dataclass
from typing import Dict, List, Literal, Optional

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
class MovieMetadata:
    title: str
    description: str
    audience_score_average_rating: Optional[float]
    audience_score_liked_count: Optional[int]
    audience_score_not_liked_count: Optional[int]
    audience_score_review_count: Optional[int]
    audience_score_score: Optional[int]
    audience_score_sentiment: Optional[str]
    critic_score_average_rating: Optional[float]
    critic_score_liked_count: Optional[int]
    critic_score_not_liked_count: Optional[int]
    critic_score_review_count: Optional[int]
    critic_score_score: Optional[int]
    critic_score_sentiment: Optional[str]
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


def export_data_to_csv(data: Dict[str, MovieMetadata], filename: str) -> None:
    with open(filename, "w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(
            [
                "id",
                "title",
                "description",
                "audience_score_average_rating",
                "audience_score_liked_count",
                "audience_score_not_liked_count",
                "audience_score_review_count",
                "audience_score_score",
                "audience_score_sentiment",
                "critic_score_average_rating",
                "critic_score_liked_count",
                "critic_score_not_liked_count",
                "critic_score_review_count",
                "critic_score_score",
                "critic_score_sentiment",
                "director",
                "producer",
                "screenwriter",
                "distributor",
                "production_company",
                "genre",
                "sound_mix",
                "rating",
                "original_language",
                "release_date_theater",
                "release_date_streaming",
                "runtime",
                "box_office",
            ]
        )
        for id, media in data.items():
            writer.writerow(
                [
                    id,
                    media.title,
                    media.description,
                    media.audience_score_average_rating,
                    media.audience_score_liked_count,
                    media.audience_score_not_liked_count,
                    media.audience_score_review_count,
                    media.audience_score_score,
                    media.audience_score_sentiment,
                    media.critic_score_average_rating,
                    media.critic_score_liked_count,
                    media.critic_score_not_liked_count,
                    media.critic_score_review_count,
                    media.critic_score_score,
                    media.critic_score_sentiment,
                    media.director,
                    media.producer,
                    media.screenwriter,
                    media.distributor,
                    media.production_company,
                    media.genre,
                    media.sound_mix,
                    media.rating,
                    media.original_language,
                    media.release_date_theater,
                    media.release_date_streaming,
                    media.runtime,
                    media.box_office,
                ]
            )


def parse_currency_to_number(text: str) -> Optional[int]:
    # Regular expression to match a currency value with an optional M/B suffix
    pattern = r"[\$\€\£\¥]\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)([MBK]?)"
    match = re.search(pattern, text)
    if match:
        amount, multiplier = match.groups()
        number = float(amount.replace(",", ""))
        # Adjust number based on the multiplier
        if multiplier == "M":
            number *= 1_000_000
        elif multiplier == "B":
            number *= 1_000_000_000
        elif multiplier == "K":
            number *= 1_000
        return int(number)
    return None


def create_url(
    category: Category,
    sorting: Sorting,
    genre: Genre,
    rating: Rating,
) -> str:
    return f"{BASE_URL}/browse/{category}/genres:{genre}~ratings:{rating}~{sorting}"


def format_media_url(id: str) -> str:
    return f"{BASE_URL}/m/{id}"
