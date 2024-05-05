import json
from typing import List, Literal

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from helpers.media import parse_media_html
from helpers.utils import (
    BASE_URL,
    CATEGORIES,
    GENRES,
    MAX_PAGES,
    RATINGS,
    SORTINGS,
    Category,
    Genre,
    Rating,
    Sorting,
    create_url,
)


def get_media_urls():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options,
    )

    def _get_media_urls(
        category: Category, sorting: Sorting, genre: Genre, rating: Rating
    ):
        url = create_url(category, sorting, genre, rating)
        driver.get(url)

        print(url)

        for i in range(1, MAX_PAGES):
            with open(
                f"output/{category}_{sorting}_{genre}_{rating}_{i}.html", "w"
            ) as file:
                file.write(driver.page_source)

            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, 'button[data-qa="dlp-load-more-button"]')
                    )
                )
                load_more_button.click()
            except Exception:
                break

    for category in CATEGORIES:
        for sorting in SORTINGS:
            for genre in GENRES:
                for rating in RATINGS:
                    _get_media_urls(category, sorting, genre, rating)

    driver.quit()


def main() -> None:
    get_media_urls()

    # with open("movies_at_home.html") as file:
    #     html = file.read()

    # soup = BeautifulSoup(html, "html.parser")

    # for div in soup.find_all("div", {"class": "flex-container"}):
    #     name = str(
    #         div.find("span", {"data-qa": "discovery-media-list-item-title"}).text
    #     ).strip()
    #     relative_url = div.find("a")["href"]
    #     url = f"{BASE_URL}{relative_url}"

    #     print(name, url)


if __name__ == "__main__":
    main()
