import json
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from helpers.utils import MovieMetadata, format_media_url, parse_currency_to_number


def parse_movie_info(soup: BeautifulSoup, field: str) -> Optional[str]:
    for div in soup.find_all("div", {"class": "category-wrap"}):
        if field in str(div.find("rt-text", {"class": "key"}).text):
            if div.find("dd").find("rt-text"):
                return div.find("dd").find("rt-text").text
            elif div.find("dd").find("rt-link"):
                return div.find("dd").find("rt-link").text
    return None


def parse_movie_info_list(soup: BeautifulSoup, filter: str) -> Optional[List[str]]:
    for div in soup.find_all("div", {"class": "category-wrap"}):
        if filter in str(div.find("rt-text", {"class": "key"}).text):
            res = []
            for genre in div.find("dd").find_all("rt-link"):
                if genre.get("class") != ["delimiter"]:
                    res.append(genre.text)

            for genre in div.find("dd").find_all("rt-text"):
                if genre.get("class") != ["delimiter"]:
                    res.append(genre.text)
            return res

    return None


def parse_media_html(html: str) -> MovieMetadata:
    soup = BeautifulSoup(html, "html.parser")

    ratings = json.loads(soup.find("script", {"id": "media-scorecard-json"}).text)  # type: ignore

    title = soup.find("h1", {"slot": "titleIntro"}).find("span").text  # type: ignore
    description = ratings["description"]

    audience_score = None
    critic_score = None

    if "audienceScore" in ratings:
        audience_score_average_rating = ratings["audienceScore"]["averageRating"]
        audience_score_liked_count = ratings["audienceScore"]["likedCount"]
        audience_score_not_liked_count = ratings["audienceScore"]["notLikedCount"]
        audience_score_review_count = ratings["audienceScore"]["reviewCount"]
        audience_score_score = ratings["audienceScore"]["score"]
        audience_score_sentiment = ratings["audienceScore"]["sentiment"]
    else:
        audience_score_average_rating = None
        audience_score_liked_count = None
        audience_score_not_liked_count = None
        audience_score_review_count = None
        audience_score_score = None
        audience_score_sentiment = None

    if "criticsScore" in ratings:
        critic_score_average_rating = ratings["criticsScore"]["averageRating"]
        critic_score_liked_count = ratings["criticsScore"]["likedCount"]
        critic_score_not_liked_count = ratings["criticsScore"]["notLikedCount"]
        critic_score_review_count = ratings["criticsScore"]["reviewCount"]
        critic_score_score = ratings["criticsScore"]["score"]
        critic_score_sentiment = ratings["criticsScore"]["sentiment"]
    else:
        critic_score_average_rating = None
        critic_score_liked_count = None
        critic_score_not_liked_count = None
        critic_score_review_count = None
        critic_score_score = None
        critic_score_sentiment = None

    box_office = parse_movie_info(soup, "Box Office")
    if box_office is not None:
        box_office = parse_currency_to_number(box_office)

    return MovieMetadata(
        title=title,
        description=description,
        audience_score_average_rating=audience_score_average_rating,
        audience_score_liked_count=audience_score_liked_count,
        audience_score_not_liked_count=audience_score_not_liked_count,
        audience_score_review_count=audience_score_review_count,
        audience_score_score=audience_score_score,
        audience_score_sentiment=audience_score_sentiment,
        critic_score_average_rating=critic_score_average_rating,
        critic_score_liked_count=critic_score_liked_count,
        critic_score_not_liked_count=critic_score_not_liked_count,
        critic_score_review_count=critic_score_review_count,
        critic_score_score=critic_score_score,
        critic_score_sentiment=critic_score_sentiment,
        director=parse_movie_info_list(soup, "Director"),
        distributor=parse_movie_info_list(soup, "Distributor"),
        production_company=parse_movie_info_list(soup, "Production Co"),
        rating=parse_movie_info(soup, "Rating"),
        genre=parse_movie_info_list(soup, "Genre"),
        original_language=parse_movie_info(soup, "Original Language"),
        release_date_theater=parse_movie_info(soup, "Release Date (Theaters)"),
        release_date_streaming=parse_movie_info(soup, "Release Date (Streaming)"),
        runtime=parse_movie_info(soup, "Runtime"),
        sound_mix=parse_movie_info_list(soup, "Sound Mix"),
        producer=parse_movie_info_list(soup, "Producer"),
        screenwriter=parse_movie_info_list(soup, "Screenwriter"),
        box_office=box_office,
    )


def parse_media(id: str) -> MovieMetadata:
    r = requests.get(format_media_url(id))
    r.raise_for_status()

    return parse_media_html(r.text)
