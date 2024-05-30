import os
import pickle
import signal
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from helpers.media import parse_media, parse_media_html
from helpers.utils import (
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

NUM_THREADS = 30
BATCH_SIZE = 200


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


def process_movie(movie_id, movie_media, movie_media_mutex: Lock):
    try:
        media = parse_media(movie_id)
        movie_media_mutex.acquire()
        movie_media[movie_id] = media
        movie_media_mutex.release()
        return True, movie_id
    except Exception as e:
        return False, movie_id


def save_data(movie_media, save_file_path):
    with open(save_file_path + ".tmp", "wb") as file:
        pickle.dump(movie_media, file)

    os.rename(save_file_path + ".tmp", save_file_path)


def handle_exit(signum, frame, executor, movie_media, save_file_path):
    print("\nTermination signal received. Saving data before exit...")
    save_data(movie_media, save_file_path)
    executor.shutdown(wait=False)
    print("Data saved. Exiting.")
    os._exit(0)


def main() -> None:
    movie_ids = set()
    with open("movie_ids.pickle", "rb") as file:
        movie_ids = pickle.load(file)

    if os.path.exists("movie_metadata.pkl"):
        with open("movie_metadata.pkl", "rb") as file:
            movie_media = pickle.load(file)
    else:
        movie_media = {}

    movie_media_mutex = Lock()
    error_count = 0
    save_file_path = "movie_metadata.pkl"

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(
                process_movie, movie_id, movie_media, movie_media_mutex
            ): movie_id
            for movie_id in movie_ids
            if movie_id not in movie_media
        }

        # Register the signal handler
        signal.signal(
            signal.SIGINT,
            lambda signum, frame: handle_exit(
                signum, frame, executor, movie_media, save_file_path
            ),
        )

        for idx, future in enumerate(as_completed(futures)):
            success, movie_id = future.result()
            if not success:
                error_count += 1

            if (idx + 1) % BATCH_SIZE == 0:
                movie_media_mutex.acquire()
                save_data(movie_media, save_file_path)
                movie_media_mutex.release()
                print(
                    f"ERROR PERCENTAGE: {(error_count / (idx + 1)) * 100}%, Processed {idx + 1} movies, error count: {error_count}, movies saved: {len(movie_media)}"
                )

    save_data(movie_media, save_file_path)
    print(f"Error count: {error_count}")

    # for idx, movie_id in enumerate(movie_ids):
    #     if movie_id in movie_media:
    #         continue

    #     try:
    #         media = parse_media(movie_id)
    #         # time.sleep(0.2)
    #         movie_media[movie_id] = media
    #     except Exception as e:
    #         error_count += 1
    #         continue

    #     if (idx + 1) % batch_size == 0:
    #         with open(save_file_path, "wb") as file:
    #             pickle.dump(movie_media, file)

    #         print(
    #             f"ERROR PERCENTAGE: {(error_count / (idx + 1)) * 100}%, Processed {idx + 1} movies, error count: {error_count}, movies saved: {len(movie_media)}"
    #         )

    # with open(save_file_path, "wb") as file:
    #     pickle.dump(movie_media, file)

    # print(f"Error count: {error_count}")


if __name__ == "__main__":
    main()
