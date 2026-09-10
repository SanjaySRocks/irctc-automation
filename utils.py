import re


def extract_station_name(text):

    # Remove time like: 22:10 |
    text = re.sub(
        r"\d{1,2}:\d{2}\s*\|",
        "",
        text
    )

    # Remove date like: | Sat, 05 Sep
    text = re.sub(
        r"\|\s*[A-Za-z]{3},.*$",
        "",
        text
    )

    return text.strip()
