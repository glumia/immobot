#!/usr/bin/env python
import json
import os
from datetime import datetime, timezone
from re import sub
from time import sleep

import requests
from telegram.bot import Bot


def fetch_ads(url, sleep_secs=1):
    """Fetch all the ads of a search on Immobiliare.

    :param url: the `https://www.immobiliare.it/api-next/search-list/real-estates/?...`
        url of your search. Use your browser's developer tools to get this one.
    :param sleep_secs: sleep time between requests to avoid rate limits.
    :return: a list of ads.
    """
    url = sub(r"&pag=\d+", "", url)
    pag = 1
    ads = []
    while True:
        resp = requests.get(url + f"&pag={pag}").json()
        ads += resp["results"]
        if not resp["seoData"]["nextPage"]:
            break
        pag += 1
        sleep(sleep_secs)
    return ads


def main():
    url = os.environ["IMMOBOT_URL"]
    bot = Bot(os.environ["IMMOBOT_TOKEN"])

    try:
        with open("db.json", "r") as fp:
            db = json.load(fp)
    except FileNotFoundError:
        db = {}

    print(f"{datetime.now(timezone.utc).isoformat()} Fetching ads.")
    ads = fetch_ads(url)

    known_ads = db.get(url, {})
    new_ads = {}
    for ad in ads:
        id_ = str(ad["realEstate"]["id"])  # json.dump converts `int` keys to `str`.
        if id_ not in known_ads:
            new_ads[id_] = ad

    if not new_ads:
        print(f"{datetime.now(timezone.utc).isoformat()} No new ads, nothing to do.")
        return

    print(f"{datetime.now(timezone.utc).isoformat()} Updating ads database.")
    known_ads.update(new_ads)
    db[url] = known_ads
    with open("db.json", "w") as fp:
        json.dump(db, fp)

    print(f"{datetime.now(timezone.utc).isoformat()} Sending notification.")
    bot.send_message(
        os.environ["IMMOBOT_CHAT_ID"],
        "There are new ads on Immobiliare!\n"
        + "\n".join(f"- {ad['seo']['url']}" for ad in new_ads.values()),
        disable_web_page_preview=True,
    )


if __name__ == "__main__":
    main()
