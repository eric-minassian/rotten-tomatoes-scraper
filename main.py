import logging
import os
import pickle

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from helpers.media import parse_media, parse_media_html
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
    # get_media_urls()

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

    # movie_ids = set()

    # with open("/home/eric/Downloads/rotten_tomatoes_movies.csv") as file:
    #     # Skip the header
    #     file.readline()

    #     for line in file:
    #         movie_id = line.split(",")[0]
    #         movie_ids.add(movie_id)

    # print(f"Found {len(movie_ids)} movie ids")

    # # Save the movie_ids to a file
    # with open("movie_ids.pickle", "wb") as file:
    #     pickle.dump(movie_ids, file)

    movie_ids = set()
    with open("movie_ids_2.pickle", "rb") as file:
        movie_ids = pickle.load(file)

    if os.path.exists("movie_metadata.pkl"):
        with open("movie_metadata.pkl", "rb") as file:
            movie_media = pickle.load(file)
    else:
        movie_media = {}

    error_count = 0
    batch_size = 25
    save_file_path = "movie_metadata.pkl"

    for idx, movie_id in enumerate(movie_ids):
        if movie_id in movie_media:
            continue

        try:
            media = parse_media(movie_id)
            # time.sleep(0.2)
            movie_media[movie_id] = media
        except Exception as e:
            error_count += 1
            continue

        if (idx + 1) % batch_size == 0:
            with open(save_file_path, "wb") as file:
                pickle.dump(movie_media, file)

            print(
                f"ERROR PERCENTAGE: {(error_count / (idx + 1)) * 100}%, Processed {idx + 1} movies, error count: {error_count}, movies saved: {len(movie_media)}"
            )

    with open(save_file_path, "wb") as file:
        pickle.dump(movie_media, file)

    print(f"Error count: {error_count}")


if __name__ == "__main__":
    main()
