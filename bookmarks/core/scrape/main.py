from bs4 import BeautifulSoup

import googleapiclient.discovery
import googleapiclient.errors

import functools
import os
import sys
import trafilatura

from .download import fetch_url

PATTERNS = {}


MAX_CONTENT_FIELD_LEN = 1000000

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


def get_html(url):
    return BeautifulSoup(fetch_url(url), "html.parser")


def get_json(url):
    return fetch_url(url).json()


def default_scraper(url, soup=None):
    return trafilatura.extract(fetch_url(url))


def scraper(html, patterns):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(url):
            if html:
                soup = get_html(url)
            try:
                return func(url, soup) if html else func(url)
            except Exception as e:
                print(
                    f"falling back to html scraping for '{url}': {e}", file=sys.stderr
                )
                return default_scraper(url, soup=soup)

        for pattern in patterns:
            PATTERNS[pattern] = wrapper
        return wrapper

    return decorator


@scraper(html=True, patterns=["https://cheatsheetseries.owasp.org/cheatsheets/"])
def owasp_cheatsheets_scraper(url, soup):
    return soup.find_all("article")[0].text


#@scraper(html=False, patterns=["https://www.reddit.com/r/"])
#def reddit_scraper(url):
#    json = get_json(url + "/.json")
#    return json[0]["data"]["children"][0]["data"]["selftext"]



@scraper(html=True, patterns=["https://en.wikipedia.org/wiki/"])
def wikipedia_scraper(url, soup):
    title = soup.find(id="firstHeading")
    body = soup.find(id="mw-content-text")
    for el, class_ in [
        ("div", "toc"),
        ("table", "metadata"),
        ("table", "vertical-navbox"),
        ("span", "mw-editsection"),
        ("div", "printfooter"),
    ]:
        for el in body.find_all(el, class_=class_):
            el.clear()
    return title.text + "\n" + body.text


@scraper(html=False, patterns=["https://www.youtube.com/watch?v="])
def youtube_scraper(url):
    video_id = url.split("v=")[1].split("&")[0]
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", developerKey=YOUTUBE_API_KEY
    )
    request = youtube.videos().list(part="snippet,contentDetails", id=video_id)
    response = request.execute()["items"][0]["snippet"]
    return (
        response["title"]
        + "\n"
        + response["channelTitle"]
        + "\n"
        + response["description"]
    )


def scrape_content(url):
    for pattern, scraper in PATTERNS.items():
        if url.startswith(pattern):
            return scraper(url)
    return default_scraper(url)


def scrape_all(urls):
    content = ""

    for u in urls:
        if len(content) >= MAX_CONTENT_FIELD_LEN:
            break
        content = (content + "\n" + (scrape_content(u) or "")).strip()

    return content[0:MAX_CONTENT_FIELD_LEN]


def _normalise_url(url):
    for prefix, replacement in [
        ("http://indie-rpgs.com/", "http://www.indie-rpgs.com/"),
        ("https://old.reddit.com/r/", "https://www.reddit.com/r/"),
    ]:
        if url.startswith(prefix):
            return replacement + url.split(prefix)[1]
    return url

