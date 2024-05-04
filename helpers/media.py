import json
from typing import List, Optional

from bs4 import BeautifulSoup

from helpers.utils import Media, Score, parse_currency_to_number


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


def parse_media_html(html: str) -> Media:
    soup = BeautifulSoup(html, "html.parser")

    ratings = json.loads(soup.find("script", {"id": "media-scorecard-json"}).text)  # type: ignore

    title = soup.find("h1", {"slot": "titleIntro"}).find("span").text  # type: ignore
    description = ratings["description"]

    audience_score = None
    critic_score = None

    if "audienceScore" in ratings:
        audience_score = Score(
            average_rating=ratings["audienceScore"]["averageRating"],
            banded_rating_count=ratings["audienceScore"]["bandedRatingCount"],
            liked_count=ratings["audienceScore"]["likedCount"],
            not_liked_count=ratings["audienceScore"]["notLikedCount"],
            review_count=ratings["audienceScore"]["reviewCount"],
            score=ratings["audienceScore"]["score"],
            sentiment=ratings["audienceScore"]["sentiment"],
        )

    if "criticScore" in ratings:
        critic_score = Score(
            average_rating=ratings["criticScore"]["averageRating"],
            banded_rating_count=ratings["criticScore"]["bandedRatingCount"],
            liked_count=ratings["criticScore"]["likedCount"],
            not_liked_count=ratings["criticScore"]["notLikedCount"],
            review_count=ratings["criticScore"]["reviewCount"],
            score=ratings["criticScore"]["score"],
            sentiment=ratings["criticScore"]["sentiment"],
        )

    box_office = parse_movie_info(soup, "Box Office")
    if box_office is not None:
        box_office = parse_currency_to_number(box_office)

    return Media(
        title=title,
        description=description,
        audience_score=audience_score,
        critic_score=critic_score,
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
