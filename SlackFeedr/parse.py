import feedparser
from htmlslacker import HTMLSlacker
import pprint

"""valid feed requirements

RSS:
    https://feedforall.com/rss-fields.htm

    required:
        Title
        Description
        Link (possibly optional?)

ATOM:
    https://validator.w3.org/feed/docs/atom.html#requiredFeedElements

    required:
        id: (similar to link)
        Title:
        updated:

Note:
    pubdate is optional for RSS??
"""


def test_rss_feed(feed_url):
    feed_dump = feedparser.parse(feed_url).feed
    if "title" in feed_dump:
        # pprint.pprint(feedparser.parse(feed_url).feed)
        d = feedparser.parse(feed_url)
        dumpout = {
            "status": True,
            "title": feed_dump["title"],
            "feed_subtext": feed_dump["subtitle"],
            "feed_summary": HTMLSlacker(d.entries[0]["summary"]).get_output(),
            "feed_entry_link": d.entries[0]["link"],
        }
        return dumpout
    else:
        return {"status": False}


# def test_atom_feed(feed_url):
#     try:
#         print(feed_url)

#     return "blah"


feed = []


def add_feed():
    for item in feed:
        try:
            feedparser.parse(item)
            val = feedparser.parse(feed_url).feed["updated"]
        except:
            print("no items found")
    print("successfull added all items")
