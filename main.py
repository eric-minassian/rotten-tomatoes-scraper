import requests

from helpers.media import parse_media_html


def main() -> None:
    url = "https://www.rottentomatoes.com/m/avengers_endgame"
    response = requests.get(url)

    if response.status_code == 200:
        print(parse_media_html(response.text))


if __name__ == "__main__":
    main()
